import json
import re
import unicodedata
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction as db_transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.finance.models import (
    Account,
    Budget,
    Category,
    FinancialGoal,
    RecurringTransaction,
    Transaction,
)
from config.ui_texts import get_lang_from_request, get_ui_texts, tr

User = get_user_model()


CATEGORY_ALIAS_LIBRARY = {
    "shopping": [
        "shopping", "mua sam", "mua", "quan ao", "ao", "giay", "dep",
        "my pham", "phu kien", "clothes", "shirt", "pants", "dress",
        "jeans", "shoes", "bag", "tui", "son", "ao mua",
    ],
    "food": [
        "food", "an", "an uong", "an sang", "an trua", "an toi",
        "com", "pho", "bun", "do an", "lunch", "dinner", "breakfast",
        "meal", "groceries", "grocery", "do an", "tien do an",
    ],
    "coffee": [
        "coffee", "cafe", "ca phe", "tra sua", "matcha", "tra",
        "milktea", "uong cafe", "uong ca phe",
    ],
    "transport": [
        "transport", "di chuyen", "xang", "do xang", "grab", "taxi",
        "xe", "gui xe", "do xe", "parking", "bus", "fuel",
    ],
    "bills": [
        "bill", "bills", "hoa don", "dien", "nuoc", "internet",
        "wifi", "tien nha", "rent", "phone", "hoc phi",
    ],
    "salary": ["salary", "luong", "luong cung"],
    "bonus": ["bonus", "thuong"],
    "freelance": ["freelance", "lam them", "du an", "project", "side job"],
    "entertainment": ["entertainment", "giai tri", "movie", "xem phim", "netflix", "spotify", "game"],
}


def normalize_text(value):
    if not value:
        return ""
    value = unicodedata.normalize("NFD", str(value).lower())
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def contains_phrase(text, phrase):
    if not text or not phrase:
        return False
    pattern = r"(^|\s)" + re.escape(phrase) + r"(\s|$)"
    return re.search(pattern, text) is not None


def clean_remaining_text(text):
    if not text:
        return ""
    cleaned = re.sub(
        r"^\s*(tien|tiền|khoan|khoản|mon|món|cai|cái|chi|thu|cho)\s+",
        "",
        str(text),
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -,:;")
    return cleaned


def parse_amount_from_text(text):
    if not text:
        return None, ""

    raw = str(text).strip()
    amount_pattern = re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(triệu|trieu|nghìn|nghin|ngàn|ngan|tr|k|m)?",
        re.IGNORECASE,
    )
    match = amount_pattern.search(raw)

    if not match:
        return None, text

    number_text = match.group(1).replace(",", ".")
    suffix = normalize_text(match.group(2) or "")

    value = Decimal(number_text)
    multiplier = Decimal("1")

    if suffix == "k":
        multiplier = Decimal("1000")
    elif suffix in ["tr", "trieu", "m"]:
        multiplier = Decimal("1000000")
    elif suffix in ["nghin", "ngan"]:
        multiplier = Decimal("1000")

    amount = (value * multiplier).quantize(Decimal("1"))
    remaining = (raw[:match.start()] + " " + raw[match.end():]).strip()
    remaining = clean_remaining_text(remaining)
    return amount, remaining


def guess_transaction_type(normalized_text):
    transfer_keywords = ["chuyen", "transfer", "rut", "nap", "topup", "top up"]
    income_keywords = ["luong", "salary", "thuong", "bonus", "freelance", "income", "thu"]

    if any(word in normalized_text for word in transfer_keywords):
        return "transfer"
    if any(word in normalized_text for word in income_keywords):
        return "income"
    return "expense"


def find_account_from_text(user, normalized_text):
    accounts = Account.objects.filter(user=user, is_active=True)
    best_match = None
    best_score = 0

    for acc in accounts:
        candidates = [acc.name]
        if acc.bank_name:
            candidates.append(acc.bank_name)

        for item in candidates:
            normalized_item = normalize_text(item)
            if normalized_item and normalized_item in normalized_text:
                score = len(normalized_item)
                if score > best_score:
                    best_match = acc
                    best_score = score

    return best_match


def get_category_aliases(category):
    normalized_name = normalize_text(category.name)
    aliases = {normalized_name}

    if category.parent:
        aliases.add(normalize_text(category.parent.name))

    for part in normalized_name.split():
        if len(part) >= 2:
            aliases.add(part)

    for canonical, words in CATEGORY_ALIAS_LIBRARY.items():
        if canonical in normalized_name or any(
            word == normalized_name or word in normalized_name or normalized_name in word
            for word in words
        ):
            aliases.update(words)

    return [alias for alias in aliases if alias]


def find_category_from_text(user, tx_type, normalized_text):
    categories = Category.objects.filter(user=user, is_active=True, type=tx_type)

    best_match = None
    best_score = 0

    for cat in categories:
        score = 0
        normalized_name = normalize_text(cat.name)

        if contains_phrase(normalized_text, normalized_name):
            score += 12

        aliases = get_category_aliases(cat)
        for alias in aliases:
            if contains_phrase(normalized_text, alias):
                score += max(3, len(alias.split()) * 3)

        if score > best_score:
            best_score = score
            best_match = cat

    if best_score >= 3:
        return best_match

    return None


def get_history_based_suggestion(user, tx_type, normalized_text):
    if not normalized_text:
        return None, None

    words = [w for w in normalized_text.split() if len(w) >= 2]
    if not words:
        return None, None

    recent = (
        Transaction.objects.filter(user=user, type=tx_type)
        .exclude(notes__istartswith="Quick Add:")
        .select_related("account", "category")
        .order_by("-occurred_at")[:50]
    )

    best_tx = None
    best_score = 0

    for tx in recent:
        haystack = normalize_text(
            f"{tx.notes or ''} {tx.category.name if tx.category else ''} {tx.account.name if tx.account else ''}"
        )
        score = 0
        for word in words:
            if contains_phrase(haystack, word):
                score += 1

        if score > best_score:
            best_score = score
            best_tx = tx

    if best_tx and best_score >= 2:
        return best_tx.category, best_tx.account

    return None, None


def choose_default_account(user, tx_type, amount=None, exclude_account_id=None):
    accounts = list(Account.objects.filter(user=user, is_active=True))
    if exclude_account_id:
        accounts = [a for a in accounts if a.id != exclude_account_id]

    if not accounts:
        return None

    recent = (
        Transaction.objects.filter(user=user, type=tx_type)
        .select_related("account")
        .order_by("-occurred_at")
        .first()
    )
    if recent and recent.account in accounts:
        return recent.account

    if tx_type == "income":
        bank_accounts = [a for a in accounts if a.type == "bank"]
        return max(bank_accounts or accounts, key=lambda a: a.balance)

    if tx_type == "expense":
        if amount and amount <= Decimal("200000"):
            preferred = [a for a in accounts if a.type in ["cash", "e-wallet"]]
            if preferred:
                return max(preferred, key=lambda a: a.balance)
        return max(accounts, key=lambda a: a.balance)

    if tx_type == "transfer":
        bank_accounts = [a for a in accounts if a.type == "bank"]
        return max(bank_accounts or accounts, key=lambda a: a.balance)

    return accounts[0]


def create_transaction_and_update_balances(
    user,
    tx_type,
    amount,
    account,
    destination_account=None,
    category=None,
    notes="",
    occurred_at=None,
):
    if occurred_at is None:
        occurred_at = timezone.now()

    with db_transaction.atomic():
        tx = Transaction(
            user=user,
            account=account,
            destination_account=destination_account if tx_type == "transfer" else None,
            category=category if tx_type != "transfer" else None,
            type=tx_type,
            amount=amount,
            notes=notes,
            occurred_at=occurred_at,
        )
        tx.full_clean()
        tx.save()

        if tx_type == "income":
            account.balance += amount
            account.save(update_fields=["balance"])
        elif tx_type == "expense":
            account.balance -= amount
            account.save(update_fields=["balance"])
        elif tx_type == "transfer" and destination_account:
            account.balance -= amount
            destination_account.balance += amount
            account.save(update_fields=["balance"])
            destination_account.save(update_fields=["balance"])

    return tx


def get_user_category_names(user, tx_type):
    return list(
        Category.objects.filter(
            user=user,
            is_active=True,
            type=tx_type,
        ).order_by("name").values_list("name", flat=True)
    )


def quick_add_transaction(user, request, quick_text):
    amount, remaining_text = parse_amount_from_text(quick_text)
    if not amount or amount <= 0:
        raise ValueError(tr(request, "quick_add_need_amount"))

    normalized_text = normalize_text(remaining_text)
    tx_type = guess_transaction_type(normalized_text)
    matched_account = find_account_from_text(user, normalized_text)

    if tx_type == "transfer":
        destination_account = matched_account
        if not destination_account:
            raise ValueError(tr(request, "quick_add_no_target_account"))

        source_account = choose_default_account(
            user=user,
            tx_type="transfer",
            amount=amount,
            exclude_account_id=destination_account.id,
        )

        if not source_account:
            raise ValueError(tr(request, "quick_add_no_source_account"))

        if source_account.balance < amount:
            raise ValueError(tr(request, "quick_add_not_enough_source_balance"))

        return create_transaction_and_update_balances(
            user=user,
            tx_type="transfer",
            amount=amount,
            account=source_account,
            destination_account=destination_account,
            category=None,
            notes=f"Quick Add: {quick_text}",
        )

    matched_category = find_category_from_text(user, tx_type, normalized_text)
    history_category, history_account = get_history_based_suggestion(user, tx_type, normalized_text)

    category = matched_category or history_category
    account = matched_account or history_account or choose_default_account(user, tx_type, amount)

    if not account:
        raise ValueError(tr(request, "quick_add_no_account"))

    display_text = clean_remaining_text(remaining_text) or quick_text

    if tx_type == "expense":
        if not category:
            available_categories = get_user_category_names(user, "expense")
            if available_categories:
                raise ValueError(
                    tr(
                        request,
                        "quick_add_no_expense_category",
                        text=display_text,
                        categories=", ".join(available_categories[:6]),
                    )
                )
            raise ValueError(tr(request, "quick_add_need_create_expense_category"))

        if account.balance < amount:
            raise ValueError(tr(request, "quick_add_not_enough_balance"))

    if tx_type == "income":
        if not category:
            available_categories = get_user_category_names(user, "income")
            if available_categories:
                raise ValueError(
                    tr(
                        request,
                        "quick_add_no_income_category",
                        text=display_text,
                        categories=", ".join(available_categories[:6]),
                    )
                )
            raise ValueError(tr(request, "quick_add_need_create_income_category"))

    return create_transaction_and_update_balances(
        user=user,
        tx_type=tx_type,
        amount=amount,
        account=account,
        destination_account=None,
        category=category,
        notes=f"Quick Add: {quick_text}",
    )


def build_quick_templates(user):
    recent = (
        Transaction.objects.filter(user=user)
        .select_related("account", "destination_account", "category")
        .order_by("-occurred_at")[:20]
    )

    seen = set()
    templates = []

    for tx in recent:
        key = (
            tx.type,
            tx.category_id,
            tx.account_id,
            tx.destination_account_id,
            str(tx.amount),
            (tx.notes or "").strip(),
        )
        if key in seen:
            continue
        seen.add(key)

        if tx.type == "transfer" and tx.destination_account:
            title = f"Transfer → {tx.destination_account.name}"
        elif tx.category:
            title = tx.category.name
        else:
            title = tx.type.title()

        subtitle = f"{int(tx.amount):,} • {tx.account.name}"

        templates.append(
            {
                "id": tx.id,
                "title": title,
                "subtitle": subtitle,
                "type": tx.type,
            }
        )

        if len(templates) >= 6:
            break

    return templates


def build_recurring_suggestions(user):
    txs = list(
        Transaction.objects.filter(user=user, type__in=["income", "expense"])
        .select_related("account", "category")
        .order_by("-occurred_at")[:100]
    )

    grouped = {}
    for tx in txs:
        key = (
            tx.type,
            tx.category_id,
            tx.account_id,
            str(tx.amount),
            (tx.notes or "").strip().lower(),
        )
        grouped.setdefault(key, []).append(tx)

    recurring = []
    for items in grouped.values():
        if len(items) < 2:
            continue

        dates = sorted([tx.occurred_at.date() for tx in items])
        gaps = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]

        if any(20 <= gap <= 40 for gap in gaps):
            latest = max(items, key=lambda t: t.occurred_at)
            recurring.append(
                {
                    "id": latest.id,
                    "title": latest.category.name if latest.category else latest.type.title(),
                    "subtitle": f"{int(latest.amount):,} • {latest.account.name}",
                    "type": latest.type,
                }
            )

    recurring.sort(key=lambda x: x["title"])
    return recurring[:4]


def set_language_view(request, code):
    if code not in ("vi", "en"):
        code = "vi"
    request.session["lang"] = code
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/dashboard/"
    return redirect(next_url)


def landing_page_view(request):
    return render(request, "web/landingpage.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")

        messages.error(request, tr(request, "invalid_login"))

    return render(request, "web/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        display_name = request.POST.get("display_name", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not password:
            messages.error(request, tr(request, "register_required"))
            return render(request, "web/register.html")

        if password != confirm_password:
            messages.error(request, tr(request, "password_mismatch"))
            return render(request, "web/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, tr(request, "username_exists"))
            return render(request, "web/register.html")

        if email and User.objects.filter(email=email).exists():
            messages.error(request, tr(request, "email_exists"))
            return render(request, "web/register.html")

        user = User.objects.create_user(username=username, email=email, password=password)

        if hasattr(user, "display_name"):
            user.display_name = display_name
            user.save(update_fields=["display_name"])

        auth_login(request, user)
        messages.success(request, tr(request, "register_success"))
        return redirect("dashboard")

    return render(request, "web/register.html")


def logout_view(request):
    auth_logout(request)
    return redirect("landing")


@login_required
def dashboard_view(request):
    user = request.user

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "quick_add":
            quick_text = request.POST.get("quick_text", "").strip()
            if not quick_text:
                messages.error(request, tr(request, "quick_add_empty"))
                return redirect("dashboard")

            try:
                tx = quick_add_transaction(user, request, quick_text)
                lang = get_lang_from_request(request)
                type_label = get_ui_texts(lang)[f"type_{tx.type}"]
                messages.success(
                    request,
                    tr(
                        request,
                        "quick_add_saved",
                        type_label=type_label,
                        amount=f"{int(tx.amount):,}",
                        account=tx.account.name,
                    ),
                )
            except Exception as e:
                messages.error(request, str(e))

            return redirect("dashboard")

        if action == "repeat":
            transaction_id = request.POST.get("transaction_id")
            try:
                old_tx = Transaction.objects.select_related(
                    "account", "destination_account", "category"
                ).get(id=transaction_id, user=user)

                if old_tx.type in ["expense", "transfer"] and old_tx.account.balance < old_tx.amount:
                    messages.error(request, tr(request, "quick_add_not_enough_balance"))
                    return redirect("dashboard")

                create_transaction_and_update_balances(
                    user=user,
                    tx_type=old_tx.type,
                    amount=old_tx.amount,
                    account=old_tx.account,
                    destination_account=old_tx.destination_account,
                    category=old_tx.category,
                    notes=old_tx.notes,
                    occurred_at=timezone.now(),
                )
                messages.success(request, tr(request, "repeat_success"))
            except Transaction.DoesNotExist:
                messages.error(request, tr(request, "repeat_not_found"))
            except Exception:
                messages.error(request, tr(request, "repeat_failed"))

            return redirect("dashboard")

    now = timezone.localtime()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month_start = month_start.replace(month=month_start.month + 1)

    month_transactions = Transaction.objects.filter(
        user=user,
        occurred_at__gte=month_start,
        occurred_at__lt=next_month_start,
    )

    total_income = month_transactions.filter(type="income").aggregate(
        total=Coalesce(Sum("amount"), Decimal("0"))
    )["total"]

    total_expense = month_transactions.filter(type="expense").aggregate(
        total=Coalesce(Sum("amount"), Decimal("0"))
    )["total"]

    net_savings = total_income - total_expense

    accounts = Account.objects.filter(user=user, is_active=True).order_by("-created_at")
    total_wallet_balance = sum((acc.current_balance for acc in accounts), Decimal("0"))

    recent_transactions = (
        Transaction.objects.filter(user=user)
        .select_related("account", "destination_account", "category")
        .order_by("-occurred_at")[:10]
    )

    largest_expense = month_transactions.filter(type="expense").order_by("-amount").first()
    monthly_transaction_count = month_transactions.count()
    expense_categories_used = (
        month_transactions.filter(type="expense", category__isnull=False)
        .values("category")
        .distinct()
        .count()
    )

    budgets = Budget.objects.filter(
        user=user,
        month=month_start.month,
        year=month_start.year,
    ).select_related("category")

    budget_rows = []
    for budget in budgets:
        spent = month_transactions.filter(
            type="expense",
            category=budget.category,
        ).aggregate(total=Coalesce(Sum("amount"), Decimal("0")))["total"]

        usage_percent = Decimal("0")
        if budget.amount and budget.amount > 0:
            usage_percent = (spent / budget.amount) * 100

        remaining = budget.amount - spent

        status = "safe"
        if usage_percent >= 100:
            status = "over"
        elif usage_percent >= budget.alert_threshold:
            status = "warning"

        budget_rows.append(
            {
                "budget": budget,
                "category": budget.category.name,
                "budget_amount": budget.amount,
                "spent": spent,
                "remaining": remaining,
                "usage_percent": round(usage_percent, 2),
                "status": status,
            }
        )

    budget_rows = sorted(budget_rows, key=lambda x: x["usage_percent"], reverse=True)
    warning_budget_count = sum(1 for row in budget_rows if row["status"] == "warning")
    over_budget_count = sum(1 for row in budget_rows if row["status"] == "over")

    expense_by_category = list(
        month_transactions.filter(type="expense", category__isnull=False)
        .values("category__name")
        .annotate(total=Coalesce(Sum("amount"), Decimal("0")))
        .order_by("-total")
    )

    top_expense_categories = expense_by_category[:5]
    top_expense_max = top_expense_categories[0]["total"] if top_expense_categories else Decimal("0")

    for row in top_expense_categories:
        if top_expense_max > 0:
            row["pct"] = float((row["total"] / top_expense_max) * 100)
        else:
            row["pct"] = 0

    def shift_month(dt, offset):
        month = dt.month - 1 + offset
        year = dt.year + month // 12
        month = month % 12 + 1
        return dt.replace(year=year, month=month, day=1)

    trend_points = []
    for offset in range(-5, 1):
        start = shift_month(month_start, offset)
        end = shift_month(month_start, offset + 1)

        period_qs = Transaction.objects.filter(
            user=user,
            occurred_at__gte=start,
            occurred_at__lt=end,
        )

        income_val = period_qs.filter(type="income").aggregate(
            total=Coalesce(Sum("amount"), Decimal("0"))
        )["total"]
        expense_val = period_qs.filter(type="expense").aggregate(
            total=Coalesce(Sum("amount"), Decimal("0"))
        )["total"]

        trend_points.append(
            {
                "label": f"{start.month:02d}/{start.year}",
                "income": float(income_val),
                "expense": float(expense_val),
                "net": float(income_val - expense_val),
            }
        )

    while len(trend_points) > 4 and trend_points[0]["income"] == 0 and trend_points[0]["expense"] == 0:
        trend_points.pop(0)

    trend_labels = [p["label"] for p in trend_points]
    trend_income = [p["income"] for p in trend_points]
    trend_expense = [p["expense"] for p in trend_points]
    trend_net = [p["net"] for p in trend_points]

    expense_chart_labels = [row["category__name"] for row in expense_by_category]
    expense_chart_values = [float(row["total"]) for row in expense_by_category]

    account_chart_labels = [acc.name for acc in accounts]
    account_chart_values = [float(acc.current_balance) for acc in accounts]

    budget_chart_labels = [row["category"] for row in budget_rows]
    budget_limit_values = [float(row["budget_amount"]) for row in budget_rows]
    budget_spent_values = [float(row["spent"]) for row in budget_rows]

    active_goals = FinancialGoal.objects.filter(
        user=user,
        is_active=True,
    ).order_by("deadline", "-created_at")[:3]

    recurring_due_soon = RecurringTransaction.objects.filter(
        user=user,
        is_active=True,
        next_due_date__lte=timezone.localdate() + timezone.timedelta(days=7),
    ).order_by("next_due_date")[:5]

    context = {
        "current_month": month_start.month,
        "current_year": month_start.year,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "total_wallet_balance": total_wallet_balance,
        "monthly_transaction_count": monthly_transaction_count,
        "largest_expense": largest_expense,
        "expense_categories_used": expense_categories_used,
        "warning_budget_count": warning_budget_count,
        "over_budget_count": over_budget_count,
        "accounts": accounts,
        "recent_transactions": recent_transactions,
        "budget_rows": budget_rows,
        "top_expense_categories": top_expense_categories,
        "quick_templates": build_quick_templates(user),
        "recurring_suggestions": build_recurring_suggestions(user),
        "active_goals": active_goals,
        "recurring_due_soon": recurring_due_soon,
        "trend_labels_json": json.dumps(trend_labels),
        "trend_income_json": json.dumps(trend_income),
        "trend_expense_json": json.dumps(trend_expense),
        "trend_net_json": json.dumps(trend_net),
        "expense_chart_labels_json": json.dumps(expense_chart_labels),
        "expense_chart_values_json": json.dumps(expense_chart_values),
        "account_chart_labels_json": json.dumps(account_chart_labels),
        "account_chart_values_json": json.dumps(account_chart_values),
        "budget_chart_labels_json": json.dumps(budget_chart_labels),
        "budget_limit_values_json": json.dumps(budget_limit_values),
        "budget_spent_values_json": json.dumps(budget_spent_values),
    }

    return render(request, "web/dashboard.html", context)


@login_required
def accounts_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            name = request.POST.get("name", "").strip()
            account_type = request.POST.get("type", "cash").strip()
            bank_name = request.POST.get("bank_name", "").strip()
            currency = request.POST.get("currency", "VND").strip() or "VND"
            initial_balance = request.POST.get("initial_balance", "0").strip() or "0"

            if not name:
                messages.error(request, "Account name is required.")
                return redirect("accounts")

            try:
                Account.objects.create(
                    user=request.user,
                    name=name,
                    type=account_type,
                    bank_name=bank_name if bank_name else None,
                    currency=currency,
                    initial_balance=Decimal(initial_balance),
                    balance=Decimal(initial_balance),
                )
                messages.success(request, tr(request, "create_success_account"))
            except Exception as e:
                messages.error(request, f"Could not create account: {e}")

            return redirect("accounts")

        if action == "delete":
            account_id = request.POST.get("account_id")
            try:
                account = Account.objects.get(id=account_id, user=request.user, is_active=True)
                account.delete()
                messages.success(request, tr(request, "delete_success_account"))
            except Exception as e:
                messages.error(request, f"Could not delete account: {e}")

            return redirect("accounts")

    accounts = Account.objects.filter(user=request.user, is_active=True).order_by("-created_at")

    return render(
        request,
        "web/accounts.html",
        {
            "accounts": accounts,
            "account_types": Account.TYPE_CHOICES,
        },
    )


@login_required
def categories_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            name = request.POST.get("name", "").strip()
            category_type = request.POST.get("type", "").strip()
            parent_id = request.POST.get("parent_id", "").strip()

            if not name:
                messages.error(request, "Category name is required.")
                return redirect("categories")

            if category_type not in ["income", "expense"]:
                messages.error(request, "Invalid category type.")
                return redirect("categories")

            parent = None
            if parent_id:
                try:
                    parent = Category.objects.get(id=parent_id, user=request.user, is_active=True)
                except Category.DoesNotExist:
                    messages.error(request, "Parent category not found.")
                    return redirect("categories")

            try:
                category = Category(
                    user=request.user,
                    name=name,
                    type=category_type,
                    parent=parent,
                )
                category.full_clean()
                category.save()
                messages.success(request, tr(request, "create_success_category"))
            except Exception as e:
                messages.error(request, f"Could not create category: {e}")

            return redirect("categories")

        if action == "delete":
            category_id = request.POST.get("category_id")
            try:
                category = Category.objects.get(
                    id=category_id,
                    user=request.user,
                    is_active=True,
                )
                category.delete()
                messages.success(request, tr(request, "delete_success_category"))
            except Exception as e:
                messages.error(request, f"Could not delete category: {e}")

            return redirect("categories")

    income_categories = Category.objects.filter(
        user=request.user,
        is_active=True,
        type="income",
    ).order_by("name")

    expense_categories = Category.objects.filter(
        user=request.user,
        is_active=True,
        type="expense",
    ).order_by("name")

    parent_candidates = Category.objects.filter(
        user=request.user,
        is_active=True,
    ).order_by("type", "name")

    now = timezone.localtime()
    month = now.month
    year = now.year

    def build_rows(categories_queryset):
        parents = categories_queryset.filter(parent__isnull=True)
        rows = []

        for parent in parents:
            spent = Transaction.objects.filter(
                user=request.user,
                type="expense",
                category=parent,
                occurred_at__year=year,
                occurred_at__month=month,
            ).aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]

            budget = Budget.objects.filter(
                user=request.user,
                category=parent,
                month=month,
                year=year,
            ).first()

            rows.append(
                {
                    "category": parent,
                    "level": 0,
                    "spent": spent,
                    "budget": budget,
                }
            )

            children = categories_queryset.filter(parent=parent).order_by("name")
            for child in children:
                spent_child = Transaction.objects.filter(
                    user=request.user,
                    type="expense",
                    category=child,
                    occurred_at__year=year,
                    occurred_at__month=month,
                ).aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]

                budget_child = Budget.objects.filter(
                    user=request.user,
                    category=child,
                    month=month,
                    year=year,
                ).first()

                rows.append(
                    {
                        "category": child,
                        "level": 1,
                        "spent": spent_child,
                        "budget": budget_child,
                    }
                )

        return rows

    income_rows = build_rows(income_categories)
    expense_rows = build_rows(expense_categories)

    return render(
        request,
        "web/categories.html",
        {
            "income_rows": income_rows,
            "expense_rows": expense_rows,
            "parent_candidates": parent_candidates,
            "current_month": month,
            "current_year": year,
        },
    )


@login_required
def budgets_view(request):
    now = timezone.localtime()
    current_month = now.month
    current_year = now.year

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            category_id = request.POST.get("category")
            amount = request.POST.get("amount", "0").strip()
            period = request.POST.get("period", "monthly").strip()
            month = request.POST.get("month", str(current_month)).strip()
            year = request.POST.get("year", str(current_year)).strip()
            alert_threshold = request.POST.get("alert_threshold", "80").strip()

            try:
                category = Category.objects.get(
                    id=category_id,
                    user=request.user,
                    is_active=True,
                    type="expense",
                )
            except Category.DoesNotExist:
                messages.error(request, "Expense category not found.")
                return redirect("budgets")

            try:
                budget = Budget(
                    user=request.user,
                    category=category,
                    amount=Decimal(amount),
                    period=period,
                    month=int(month),
                    year=int(year),
                    alert_threshold=Decimal(alert_threshold),
                )
                budget.full_clean()
                budget.save()
                messages.success(request, tr(request, "create_success_budget"))
            except Exception as e:
                messages.error(request, f"Could not create budget: {e}")

            return redirect("budgets")

        if action == "delete":
            budget_id = request.POST.get("budget_id")
            try:
                budget = Budget.objects.get(id=budget_id, user=request.user)
                budget.delete()
                messages.success(request, tr(request, "delete_success_budget"))
            except Exception as e:
                messages.error(request, f"Could not delete budget: {e}")

            return redirect("budgets")

    budgets = (
        Budget.objects.filter(user=request.user)
        .select_related("category")
        .order_by("-year", "-month", "category__name")
    )

    budget_rows = []
    for budget in budgets:
        spent = Transaction.objects.filter(
            user=request.user,
            type="expense",
            category=budget.category,
            occurred_at__year=budget.year,
            occurred_at__month=budget.month,
        ).aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]

        usage_percent = Decimal(0)
        if budget.amount and budget.amount > 0:
            usage_percent = (spent / budget.amount) * 100

        remaining = budget.amount - spent

        status = "safe"
        if usage_percent >= 100:
            status = "over"
        elif usage_percent >= budget.alert_threshold:
            status = "warning"

        budget_rows.append(
            {
                "budget": budget,
                "spent": spent,
                "remaining": remaining,
                "usage_percent": round(usage_percent, 2),
                "status": status,
            }
        )

    expense_categories = Category.objects.filter(
        user=request.user,
        is_active=True,
        type="expense",
    ).order_by("name")

    return render(
        request,
        "web/budgets.html",
        {
            "current_month": current_month,
            "current_year": current_year,
            "budget_rows": budget_rows,
            "expense_categories": expense_categories,
        },
    )


@login_required
def goals_view(request):
    user = request.user

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            name = request.POST.get("name", "").strip()
            target_amount = request.POST.get("target_amount", "").strip()
            current_amount = request.POST.get("current_amount", "0").strip() or "0"
            deadline = request.POST.get("deadline", "").strip()
            notes = request.POST.get("notes", "").strip()

            if not name:
                messages.error(request, "Goal name is required.")
                return redirect("goals")

            try:
                goal = FinancialGoal(
                    user=user,
                    name=name,
                    target_amount=Decimal(target_amount),
                    current_amount=Decimal(current_amount),
                    notes=notes,
                )
                if deadline:
                    goal.deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
                goal.full_clean()
                goal.save()
                messages.success(request, "Financial goal created successfully.")
            except Exception as e:
                messages.error(request, f"Could not create goal: {e}")

            return redirect("goals")

        if action == "update_progress":
            goal_id = request.POST.get("goal_id")
            add_amount = request.POST.get("add_amount", "").strip()

            try:
                goal = FinancialGoal.objects.get(id=goal_id, user=user, is_active=True)
                delta = Decimal(add_amount)
                if delta <= 0:
                    raise ValueError("Amount must be greater than 0.")

                goal.current_amount += delta
                goal.full_clean()
                goal.save(update_fields=["current_amount", "updated_at"])
                messages.success(request, "Goal progress updated successfully.")
            except Exception as e:
                messages.error(request, f"Could not update goal: {e}")

            return redirect("goals")

        if action == "delete":
            goal_id = request.POST.get("goal_id")
            try:
                goal = FinancialGoal.objects.get(id=goal_id, user=user, is_active=True)
                goal.is_active = False
                goal.save(update_fields=["is_active", "updated_at"])
                messages.success(request, "Goal deleted successfully.")
            except Exception as e:
                messages.error(request, f"Could not delete goal: {e}")

            return redirect("goals")

    goals = FinancialGoal.objects.filter(user=user, is_active=True).order_by("deadline", "-created_at")

    return render(
        request,
        "web/goals.html",
        {
            "goals": goals,
        },
    )

def create_transaction_from_recurring(recurring):
    normalized_amount = recurring.amount.quantize(Decimal("1"))

    if recurring.type in ["expense", "transfer"] and recurring.account.balance < normalized_amount:
        raise ValueError("Not enough balance in the source account.")

    tx = create_transaction_and_update_balances(
        user=recurring.user,
        tx_type=recurring.type,
        amount=normalized_amount,
        account=recurring.account,
        destination_account=recurring.destination_account,
        category=recurring.category,
        notes=recurring.notes or f"Recurring: {recurring.title}",
        occurred_at=timezone.now(),
    )

    recurring.mark_generated()
    return tx


@login_required
def recurring_view(request):
    user = request.user

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            title = request.POST.get("title", "").strip()
            tx_type = request.POST.get("type", "").strip()
            amount_raw = request.POST.get("amount", "").strip()
            account_id = request.POST.get("account", "").strip()
            destination_account_id = request.POST.get("destination_account", "").strip()
            category_id = request.POST.get("category", "").strip()
            frequency = request.POST.get("frequency", "monthly").strip()
            next_due_date_raw = request.POST.get("next_due_date", "").strip()
            auto_create = request.POST.get("auto_create") == "on"
            notes = request.POST.get("notes", "").strip()

            if not title:
                messages.error(request, "Title is required.")
                return redirect("recurring")

            try:
                amount = Decimal(amount_raw).quantize(Decimal("1"))
                if amount <= 0:
                    raise ValueError
            except Exception:
                messages.error(request, "Amount must be greater than 0.")
                return redirect("recurring")

            try:
                account = Account.objects.get(id=account_id, user=user, is_active=True)
            except Account.DoesNotExist:
                messages.error(request, "Source account not found.")
                return redirect("recurring")

            destination_account = None
            if destination_account_id:
                try:
                    destination_account = Account.objects.get(
                        id=destination_account_id,
                        user=user,
                        is_active=True,
                    )
                except Account.DoesNotExist:
                    messages.error(request, "Destination account not found.")
                    return redirect("recurring")

            category = None
            if category_id:
                try:
                    category = Category.objects.get(
                        id=category_id,
                        user=user,
                        is_active=True,
                    )
                except Category.DoesNotExist:
                    messages.error(request, "Category not found.")
                    return redirect("recurring")

            if tx_type != "transfer":
                destination_account = None

            if tx_type == "transfer":
                category = None

            if tx_type == "income" and category and category.type != "income":
                messages.error(request, "Income recurring transaction must use an income category.")
                return redirect("recurring")

            if tx_type == "expense" and category and category.type != "expense":
                messages.error(request, "Expense recurring transaction must use an expense category.")
                return redirect("recurring")

            if not next_due_date_raw:
                messages.error(request, "Next due date is required.")
                return redirect("recurring")

            try:
                next_due_date = datetime.strptime(next_due_date_raw, "%Y-%m-%d").date()
            except Exception:
                messages.error(request, "Invalid next due date.")
                return redirect("recurring")

            try:
                recurring = RecurringTransaction(
                    user=user,
                    title=title,
                    type=tx_type,
                    amount=amount,
                    account=account,
                    destination_account=destination_account,
                    category=category,
                    frequency=frequency,
                    next_due_date=next_due_date,
                    auto_create=auto_create,
                    notes=notes,
                )
                recurring.full_clean()
                recurring.save()
                messages.success(request, "Recurring transaction created successfully.")
            except Exception as e:
                messages.error(request, f"Could not create recurring transaction: {e}")

            return redirect("recurring")

        if action == "apply_now":
            recurring_id = request.POST.get("recurring_id")
            try:
                recurring = RecurringTransaction.objects.select_related(
                    "account", "destination_account", "category"
                ).get(id=recurring_id, user=user, is_active=True)

                create_transaction_from_recurring(recurring)
                messages.success(request, "Recurring transaction applied successfully.")
            except Exception as e:
                messages.error(request, f"Could not apply recurring transaction: {e}")

            return redirect("recurring")

        if action == "delete":
            recurring_id = request.POST.get("recurring_id")
            try:
                recurring = RecurringTransaction.objects.get(
                    id=recurring_id,
                    user=user,
                    is_active=True,
                )
                recurring.is_active = False
                recurring.save(update_fields=["is_active", "updated_at"])
                messages.success(request, "Recurring transaction deleted successfully.")
            except Exception as e:
                messages.error(request, f"Could not delete recurring transaction: {e}")

            return redirect("recurring")

    recurring_items = RecurringTransaction.objects.filter(
        user=user,
        is_active=True,
    ).select_related(
        "account",
        "destination_account",
        "category",
    ).order_by("next_due_date", "-created_at")

    accounts = Account.objects.filter(user=user, is_active=True).order_by("name")
    income_categories = Category.objects.filter(
        user=user,
        is_active=True,
        type="income",
    ).order_by("name")
    expense_categories = Category.objects.filter(
        user=user,
        is_active=True,
        type="expense",
    ).order_by("name")

    return render(
        request,
        "web/recurring.html",
        {
            "recurring_items": recurring_items,
            "accounts": accounts,
            "income_categories": income_categories,
            "expense_categories": expense_categories,
        },
    )

@login_required
def transactions_view(request):
    if request.method == "POST":
        action = request.POST.get("action", "create")

        if action == "create":
            tx_type = request.POST.get("type", "").strip()
            amount_raw = request.POST.get("amount", "").strip()
            category_id = request.POST.get("category", "").strip()
            account_id = request.POST.get("account", "").strip()
            destination_account_id = request.POST.get("destination_account", "").strip()
            notes = request.POST.get("notes", "").strip()
            occurred_at_raw = request.POST.get("occurred_at", "").strip()

            if tx_type not in ["income", "expense", "transfer"]:
                messages.error(request, tr(request, "invalid_transaction_type"))
                return redirect("transactions")

            try:
                amount = Decimal(amount_raw)
                if amount <= 0:
                    raise ValueError
            except Exception:
                messages.error(request, tr(request, "amount_invalid"))
                return redirect("transactions")

            try:
                account = Account.objects.get(
                    id=account_id,
                    user=request.user,
                    is_active=True,
                )
            except Account.DoesNotExist:
                messages.error(request, "Source account not found.")
                return redirect("transactions")

            category = None
            if category_id:
                try:
                    category = Category.objects.get(
                        id=category_id,
                        user=request.user,
                        is_active=True,
                    )
                except Category.DoesNotExist:
                    messages.error(request, "Category not found.")
                    return redirect("transactions")

            destination_account = None
            if destination_account_id:
                try:
                    destination_account = Account.objects.get(
                        id=destination_account_id,
                        user=request.user,
                        is_active=True,
                    )
                except Account.DoesNotExist:
                    messages.error(request, "Destination account not found.")
                    return redirect("transactions")

            if tx_type == "expense":
                if not category:
                    messages.error(request, "Expense must have a category.")
                    return redirect("transactions")
                if category.type != "expense":
                    messages.error(request, "Expense must use an expense category.")
                    return redirect("transactions")

            if tx_type == "income":
                if category and category.type != "income":
                    messages.error(request, "Income can only use an income category.")
                    return redirect("transactions")

            if tx_type == "transfer":
                if not destination_account:
                    messages.error(request, "Transfer must have a destination account.")
                    return redirect("transactions")
                if account.id == destination_account.id:
                    messages.error(request, "Source and destination accounts must be different.")
                    return redirect("transactions")
                if category:
                    messages.error(request, "Transfer should not use a category.")
                    return redirect("transactions")

            occurred_at = timezone.now()
            if occurred_at_raw:
                try:
                    occurred_at = datetime.fromisoformat(occurred_at_raw)
                    if timezone.is_naive(occurred_at):
                        occurred_at = timezone.make_aware(occurred_at)
                except Exception:
                    messages.error(request, "Invalid transaction date/time.")
                    return redirect("transactions")

            if tx_type in ["expense", "transfer"] and account.balance < amount:
                messages.error(request, tr(request, "quick_add_not_enough_balance"))
                return redirect("transactions")

            try:
                create_transaction_and_update_balances(
                    user=request.user,
                    tx_type=tx_type,
                    amount=amount,
                    account=account,
                    destination_account=destination_account,
                    category=category,
                    notes=notes,
                    occurred_at=occurred_at,
                )
                messages.success(request, tr(request, "create_success_transaction"))
            except ValidationError as e:
                if hasattr(e, "messages") and e.messages:
                    messages.error(request, e.messages[0])
                else:
                    messages.error(request, "Invalid transaction data.")
            except Exception as e:
                messages.error(request, f"Could not create transaction: {e}")

            return redirect("transactions")

        if action == "delete":
            tx_id = request.POST.get("transaction_id")

            try:
                with db_transaction.atomic():
                    tx = Transaction.objects.select_related(
                        "account", "destination_account"
                    ).get(id=tx_id, user=request.user)

                    if tx.type == "income":
                        tx.account.balance -= tx.amount
                        tx.account.save(update_fields=["balance"])
                    elif tx.type == "expense":
                        tx.account.balance += tx.amount
                        tx.account.save(update_fields=["balance"])
                    elif tx.type == "transfer" and tx.destination_account:
                        tx.account.balance += tx.amount
                        tx.destination_account.balance -= tx.amount
                        tx.account.save(update_fields=["balance"])
                        tx.destination_account.save(update_fields=["balance"])

                    tx.delete()

                messages.success(request, tr(request, "delete_success_transaction"))
            except Transaction.DoesNotExist:
                messages.error(request, "Transaction not found.")
            except Exception as e:
                messages.error(request, f"Could not delete transaction: {e}")

            return redirect("transactions")

    selected_type = request.GET.get("type", "").strip()
    selected_sort = request.GET.get("sort", "-occurred_at").strip()

    allowed_sorts = ["-occurred_at", "occurred_at", "-amount", "amount"]
    if selected_sort not in allowed_sorts:
        selected_sort = "-occurred_at"

    transactions = Transaction.objects.filter(user=request.user).select_related(
        "account", "destination_account", "category"
    )

    if selected_type in ["income", "expense", "transfer"]:
        transactions = transactions.filter(type=selected_type)

    transactions = transactions.order_by(selected_sort)

    paginator = Paginator(transactions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    accounts = Account.objects.filter(
        user=request.user,
        is_active=True,
    ).order_by("name")

    categories = Category.objects.filter(
        user=request.user,
        is_active=True,
    ).order_by("type", "name")

    return render(
        request,
        "web/transactions.html",
        {
            "page_obj": page_obj,
            "accounts": accounts,
            "categories": categories,
            "selected_type": selected_type,
            "selected_sort": selected_sort,
        },
    )