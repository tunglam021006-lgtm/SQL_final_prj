from django.contrib import admin
from .models import (
    Account,
    Category,
    Transaction,
    Budget,
    RecurringTransaction,
    FinancialGoal,
)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "type", "currency", "initial_balance", "created_at")
    search_fields = ("name", "user__username", "user__email")
    list_filter = ("type", "currency", "created_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "user", "parent")
    search_fields = ("name", "user__username")
    list_filter = ("type",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "account", "destination_account", "category", "amount", "occurred_at")
    search_fields = ("user__username", "notes")
    list_filter = ("type", "occurred_at", "category")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "amount", "period", "month", "year", "alert_threshold")
    search_fields = ("user__username", "category__name")
    list_filter = ("period", "year", "month")


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "type",
        "amount",
        "frequency",
        "next_due_date",
        "auto_create",
        "is_active",
    )
    list_filter = ("type", "frequency", "auto_create", "is_active")
    search_fields = ("title", "notes", "user__username")


@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "target_amount",
        "current_amount",
        "deadline",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "notes", "user__username")