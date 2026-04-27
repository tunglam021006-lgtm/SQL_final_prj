from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction as db_transaction
from decimal import Decimal
import datetime

from apps.finance.models import Account, Category, Transaction, Budget

User = get_user_model()


class Command(BaseCommand):
    help = "Create a demo user with realistic finance data for testing the whole system."

    TEST_USERNAME = "taikhoantest"
    TEST_PASSWORD = "demo12345"  # đổi nếu muốn
    TEST_EMAIL = "demo@expense.local"
    TEST_DISPLAY_NAME = "Demo User"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating demo dataset...")

        user, _ = User.objects.get_or_create(username=self.TEST_USERNAME)
        user.email = self.TEST_EMAIL
        if hasattr(user, "display_name"):
            user.display_name = self.TEST_DISPLAY_NAME
        user.set_password(self.TEST_PASSWORD)
        user.is_active = True
        user.save()

        self.stdout.write("Resetting old demo data...")
        Transaction.objects.filter(user=user).delete()
        Budget.objects.filter(user=user).delete()
        Category.objects.filter(user=user).delete()
        Account.objects.filter(user=user).delete()

        self.stdout.write("Creating accounts...")
        cash = Account.objects.create(
            user=user,
            name="Cash Wallet",
            type="cash",
            currency="VND",
            initial_balance=Decimal("3000000"),
        )
        bank = Account.objects.create(
            user=user,
            name="MB Bank",
            bank_name="MB Bank",
            type="bank",
            currency="VND",
            initial_balance=Decimal("15000000"),
        )
        momo = Account.objects.create(
            user=user,
            name="Momo",
            bank_name="Momo",
            type="e-wallet",
            currency="VND",
            initial_balance=Decimal("1000000"),
        )

        self.stdout.write("Creating categories...")
        salary = Category.objects.create(user=user, name="Salary", type="income")
        bonus = Category.objects.create(user=user, name="Bonus", type="income")
        freelance = Category.objects.create(user=user, name="Freelance", type="income")

        food = Category.objects.create(user=user, name="Food", type="expense")
        transport = Category.objects.create(user=user, name="Transport", type="expense")
        shopping = Category.objects.create(user=user, name="Shopping", type="expense")
        bills = Category.objects.create(user=user, name="Bills", type="expense")
        entertainment = Category.objects.create(user=user, name="Entertainment", type="expense")

        breakfast = Category.objects.create(user=user, name="Breakfast", type="expense", parent=food)
        coffee = Category.objects.create(user=user, name="Coffee", type="expense", parent=food)

        now = timezone.localtime()
        current_month = now.month
        current_year = now.year

        self.stdout.write("Creating budgets...")
        Budget.objects.create(
            user=user,
            category=food,
            amount=Decimal("3000000"),
            period="monthly",
            month=current_month,
            year=current_year,
            alert_threshold=Decimal("80.00"),
        )
        Budget.objects.create(
            user=user,
            category=transport,
            amount=Decimal("1200000"),
            period="monthly",
            month=current_month,
            year=current_year,
            alert_threshold=Decimal("80.00"),
        )
        Budget.objects.create(
            user=user,
            category=shopping,
            amount=Decimal("2000000"),
            period="monthly",
            month=current_month,
            year=current_year,
            alert_threshold=Decimal("80.00"),
        )
        Budget.objects.create(
            user=user,
            category=bills,
            amount=Decimal("1000000"),
            period="monthly",
            month=current_month,
            year=current_year,
            alert_threshold=Decimal("80.00"),
        )

        self.stdout.write("Creating current-month transactions...")

        first_day = now.replace(day=1, hour=9, minute=0, second=0, microsecond=0)

        current_month_transactions = [
            # income
            ("income", Decimal("25000000"), bank, None, salary, "Monthly salary", first_day + datetime.timedelta(days=1)),
            ("income", Decimal("3000000"), momo, None, freelance, "Freelance project", first_day + datetime.timedelta(days=5)),
            ("income", Decimal("2000000"), bank, None, bonus, "Performance bonus", first_day + datetime.timedelta(days=12)),

            # transfer
            ("transfer", Decimal("2000000"), bank, cash, None, "Withdraw cash for daily spending", first_day + datetime.timedelta(days=2)),
            ("transfer", Decimal("1000000"), bank, momo, None, "Top up e-wallet", first_day + datetime.timedelta(days=8)),

            # expense
            ("expense", Decimal("250000"), cash, None, breakfast, "Breakfasts", first_day + datetime.timedelta(days=3)),
            ("expense", Decimal("180000"), momo, None, coffee, "Coffee with friends", first_day + datetime.timedelta(days=4)),
            ("expense", Decimal("850000"), bank, None, food, "Groceries and meals", first_day + datetime.timedelta(days=7)),
            ("expense", Decimal("650000"), cash, None, transport, "Fuel and parking", first_day + datetime.timedelta(days=10)),
            ("expense", Decimal("2400000"), bank, None, shopping, "New clothes and shoes", first_day + datetime.timedelta(days=15)),
            ("expense", Decimal("900000"), bank, None, bills, "Electricity and internet", first_day + datetime.timedelta(days=18)),
            ("expense", Decimal("700000"), momo, None, entertainment, "Movie and dinner", first_day + datetime.timedelta(days=20)),
            ("expense", Decimal("450000"), bank, None, food, "Weekend family meal", first_day + datetime.timedelta(days=22)),
        ]

        for tx_type, amount, source_acc, dest_acc, category, notes, occurred_at in current_month_transactions:
            self.create_transaction(
                user=user,
                tx_type=tx_type,
                amount=amount,
                account=source_acc,
                destination_account=dest_acc,
                category=category,
                notes=notes,
                occurred_at=occurred_at,
            )

        self.stdout.write("Creating historical transactions...")
        for month_offset in [1, 2, 3, 4]:
            base_date = first_day - datetime.timedelta(days=30 * month_offset)

            historical_transactions = [
                ("income", Decimal("22000000"), bank, None, salary, f"Salary {month_offset} month(s) ago", base_date + datetime.timedelta(days=1)),
                ("expense", Decimal("1200000"), bank, None, food, f"Food spending {month_offset} month(s) ago", base_date + datetime.timedelta(days=6)),
                ("expense", Decimal("500000"), cash, None, transport, f"Transport spending {month_offset} month(s) ago", base_date + datetime.timedelta(days=10)),
                ("expense", Decimal("1300000"), bank, None, bills, f"Bills {month_offset} month(s) ago", base_date + datetime.timedelta(days=15)),
                ("transfer", Decimal("1000000"), bank, cash, None, f"Transfer {month_offset} month(s) ago", base_date + datetime.timedelta(days=20)),
            ]

            for tx_type, amount, source_acc, dest_acc, category, notes, occurred_at in historical_transactions:
                self.create_transaction(
                    user=user,
                    tx_type=tx_type,
                    amount=amount,
                    account=source_acc,
                    destination_account=dest_acc,
                    category=category,
                    notes=notes,
                    occurred_at=occurred_at,
                )

        self.stdout.write(self.style.SUCCESS("Done. Demo data created successfully."))
        self.stdout.write(self.style.SUCCESS(f"Username: {self.TEST_USERNAME}"))
        self.stdout.write(self.style.SUCCESS(f"Password: {self.TEST_PASSWORD}"))

    def create_transaction(
        self,
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