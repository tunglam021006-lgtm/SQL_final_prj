import calendar
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(update_fields=["is_active"])


class Account(SoftDeleteModel):
    TYPE_CHOICES = [
        ("cash", "Cash"),
        ("bank", "Bank Account"),
        ("e-wallet", "E-Wallet"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
    )
    name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    currency = models.CharField(max_length=10, default="VND")
    initial_balance = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self._state.adding and (self.balance is None or self.balance == 0):
            self.balance = self.initial_balance or Decimal("0")
        super().save(*args, **kwargs)

    @property
    def current_balance(self):
        return self.balance

    def __str__(self):
        return self.name


class Category(SoftDeleteModel):
    TYPE_CHOICES = [
        ("expense", "Expense"),
        ("income", "Income"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        ordering = ["type", "name"]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("expense", "Expense"),
        ("income", "Income"),
        ("transfer", "Transfer"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions_sent",
    )
    destination_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions_received",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    notes = models.TextField(blank=True, null=True)
    occurred_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at"]

    def clean(self):
        if self.amount is None or self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")

        if self.type == "transfer":
            if not self.destination_account:
                raise ValidationError("Transfer must have a destination account.")
            if self.account_id == self.destination_account_id:
                raise ValidationError("Source and destination accounts must be different.")
            if self.category_id:
                raise ValidationError("Transfer should not have a category.")

        elif self.type == "expense":
            if not self.category:
                raise ValidationError("Expense must have a category.")
            if self.category.type != "expense":
                raise ValidationError("Expense must use an expense category.")

        elif self.type == "income":
            if self.category and self.category.type != "income":
                raise ValidationError("Income can only use an income category.")

    def __str__(self):
        return f"{self.type} - {self.amount}"


class Budget(models.Model):
    PERIOD_CHOICES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="budgets",
    )
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default="monthly")
    month = models.PositiveSmallIntegerField(default=timezone.localdate().month)
    year = models.PositiveIntegerField(default=timezone.localdate().year)
    alert_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("80.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "-month", "category__name"]

    def clean(self):
        if self.amount is None or self.amount <= 0:
            raise ValidationError("Budget amount must be greater than 0.")
        if not (1 <= self.month <= 12):
            raise ValidationError("Month must be between 1 and 12.")
        if self.alert_threshold < 0 or self.alert_threshold > 100:
            raise ValidationError("Alert threshold must be between 0 and 100.")

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year}"


class RecurringTransaction(models.Model):
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("transfer", "Transfer"),
    ]

    FREQUENCY_CHOICES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recurring_transactions",
    )
    title = models.CharField(max_length=120)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=0)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="recurring_transactions",
    )
    destination_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incoming_recurring_transfers",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recurring_transactions",
    )
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default="monthly")
    next_due_date = models.DateField()
    auto_create = models.BooleanField(default=False)
    last_generated_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["next_due_date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.type})"

    def clean(self):
        if self.amount is None or self.amount <= 0:
            raise ValidationError("Recurring transaction amount must be greater than 0.")

        if self.account and self.account.user_id != self.user_id:
            raise ValidationError("Source account must belong to the same user.")

        if self.destination_account and self.destination_account.user_id != self.user_id:
            raise ValidationError("Destination account must belong to the same user.")

        if self.category and self.category.user_id != self.user_id:
            raise ValidationError("Category must belong to the same user.")

        if self.type == "transfer":
            if not self.destination_account:
                raise ValidationError("Transfer recurring transaction must have a destination account.")
            if self.account_id == self.destination_account_id:
                raise ValidationError("Source and destination account must be different.")
            if self.category_id:
                raise ValidationError("Transfer recurring transaction should not have a category.")

        elif self.type == "expense":
            if not self.category:
                raise ValidationError("Expense recurring transaction must have a category.")
            if self.category.type != "expense":
                raise ValidationError("Expense recurring transaction must use an expense category.")

        elif self.type == "income":
            if self.category and self.category.type != "income":
                raise ValidationError("Income recurring transaction can only use an income category.")

    @property
    def is_due(self):
        return self.is_active and self.next_due_date <= timezone.localdate()

    @property
    def due_in_days(self):
        return (self.next_due_date - timezone.localdate()).days

    def _add_months(self, dt, months=1):
        month_index = dt.month - 1 + months
        year = dt.year + month_index // 12
        month = month_index % 12 + 1
        day = min(dt.day, calendar.monthrange(year, month)[1])
        return dt.replace(year=year, month=month, day=day)

    def move_to_next_due_date(self):
        if self.frequency == "weekly":
            self.next_due_date = self.next_due_date + timezone.timedelta(days=7)
        else:
            self.next_due_date = self._add_months(self.next_due_date, 1)

    def mark_generated(self):
        self.last_generated_at = timezone.now()
        self.move_to_next_due_date()
        self.save(update_fields=["last_generated_at", "next_due_date", "updated_at"])


class FinancialGoal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="financial_goals",
    )
    name = models.CharField(max_length=120)
    target_amount = models.DecimalField(max_digits=14, decimal_places=2)
    current_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    deadline = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["deadline", "-created_at"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.target_amount is None or self.target_amount <= 0:
            raise ValidationError("Target amount must be greater than 0.")
        if self.current_amount is None or self.current_amount < 0:
            raise ValidationError("Current amount cannot be negative.")

    @property
    def remaining_amount(self):
        remaining = self.target_amount - self.current_amount
        return remaining if remaining > 0 else Decimal("0.00")

    @property
    def progress_percent(self):
        if not self.target_amount or self.target_amount <= 0:
            return 0
        percent = (self.current_amount / self.target_amount) * 100
        return round(min(percent, 100), 2)

    @property
    def is_completed(self):
        return self.current_amount >= self.target_amount