
from django.urls import path
from apps.web import views

urlpatterns = [
    path("", views.landing_page_view, name="landing"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("accounts/", views.accounts_view, name="accounts"),
    path("categories/", views.categories_view, name="categories"),
    path("budgets/", views.budgets_view, name="budgets"),
    path("transactions/", views.transactions_view, name="transactions"),
    path("goals/", views.goals_view, name="goals"),
    path("recurring/", views.recurring_view, name="recurring"),
    path("language/<str:code>/", views.set_language_view, name="set_language"),
]