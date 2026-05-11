<div align="center">

# 💸 Personal Finance Management System

### Project 13 – Introduction to Database System

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2.30-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-UI-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Status](https://img.shields.io/badge/Status-Academic%20Demo-success?style=for-the-badge)

**Student:** Tran Tung Lam  
**Student ID:** 11245891  
**Class:** DSEB 66B  
**GitHub Repository:** https://github.com/tunglam021006-lgtm/SQL_final_prj  
**YouTube Presentation:** https://youtu.be/2hvN03izzIY

</div>

---

## 📌 Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Main Features](#2-main-features)
- [3. Technology Stack](#3-technology-stack)
- [4. Project Structure](#4-project-structure)
- [5. Database Design Summary](#5-database-design-summary)
- [6. SQL Deliverables](#6-sql-deliverables)
- [7. SQL Query Highlights](#7-sql-query-highlights)
- [8. Local Setup Instructions](#8-local-setup-instructions)
- [9. Useful Development Commands](#9-useful-development-commands)
- [10. Demo Data Summary](#10-demo-data-summary)
- [11. Testing and Validation](#11-testing-and-validation)
- [12. Known Limitations](#12-known-limitations)
- [13. Future Improvements](#13-future-improvements)
- [14. Submission Links](#14-submission-links)
- [15. References](#15-references)

---

## 1. Project Overview

**Personal Finance Management System** is a web-based application developed for **Project 13 – Introduction to Database System**. The system helps users manage personal financial activities, including:

- income,
- expenses,
- wallets/accounts,
- spending categories,
- budgets,
- financial goals,
- recurring transactions,
- financial reports and alerts.

The project is built with **Python, Django, MySQL, Bootstrap, HTML, CSS, and JavaScript**. It demonstrates how relational database design, SQL scripting, and Python web development can work together in a complete personal finance application.

> This system is designed for academic demonstration and local use. It does not connect to real banking APIs or process real payment transactions.

---

## 2. Main Features

### 🔐 User and Authentication

- User registration and login/logout.
- User-specific financial data separation.
- Each user can manage their own wallets, categories, transactions, budgets, goals, and recurring records.

### 📊 Dashboard

- Monthly financial overview.
- Total income, total expense, net cash flow, wallet balance, transaction count, largest expense, category usage, and budget risk.
- Cashflow trend chart.
- Expense breakdown chart.
- Wallet distribution chart.
- Budget-versus-spent comparison and budget alerts.

### 👛 Wallet / Account Management

- Create and manage different account types:
  - cash,
  - bank account,
  - e-wallet.
- Track initial balance and current balance.
- Link every transaction to a source wallet/account.

### 🏷️ Category Management

- Separate income and expense categories.
- Parent-child category hierarchy.
- Example: `Food` as a parent category with `Groceries`, `Restaurant`, `Coffee`, and `Breakfast` as subcategories.
- Monthly spending by category.
- Budget mapping by category.

### 💳 Transaction Management

- Create, view, filter, sort, and delete transactions.
- Supports three transaction types:
  - income,
  - expense,
  - transfer.
- Automatic account balance updates when transactions are created or removed.

### 🎯 Budget Management

- Create monthly budgets by expense category.
- Store budget amount and alert threshold.
- Calculate spent amount, remaining amount, usage percentage, and budget status.

| Status | Meaning |
|---|---|
| ✅ Safe | Spending is below the alert threshold. |
| ⚠️ Warning | Spending reaches or exceeds the alert threshold. |
| 🚨 Over | Spending exceeds the budget amount. |

### 🏁 Financial Goals

- Create saving goals.
- Track target amount, current amount, deadline, and progress percentage.

### 🔁 Recurring Transactions

- Store repeated transactions such as salary, rent, subscriptions, gym membership, and savings transfers.
- Support manual apply action to generate actual transactions.

### 🌐 Bilingual Interface

- English/Vietnamese language toggle.
- Designed to improve usability for Vietnamese users while keeping an English interface for academic demonstration.

---

## 3. Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Database | MySQL |
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| ORM | Django ORM |
| Charts/UI | JavaScript chart components and Bootstrap-based templates |
| Version Control | Git, GitHub |
| Database Design Tools | ERDPlus, MySQL Workbench |

---

## 4. Project Structure

```text
Project-13-Personal-Finance/
│
├── apps/
│   ├── finance/                 # Finance models, migrations, seed command
│   ├── users/                   # Custom user/authentication logic
│   └── web/                     # Views, templates, dashboard, UI pages
│
├── config/                      # Django project settings and URL configuration
│
├── database/
│   ├── 01_create_database.sql
│   ├── 02_schema.sql
│   ├── 02b_schema_clean.sql
│   ├── 03_sample_data.sql
│   ├── 04_queries.sql
│   ├── 05_advanced_objects.sql
│   ├── 06_security_roles.sql
│   └── README_SQL_FILES.md
│
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

## 5. Database Design Summary

The assignment specification requires the conceptual entities:

```text
Users
Income
Expenses
ExpenseCategories
BankAccounts
```

The implemented application extends this design into a more flexible Django/MySQL schema.

| Table | Purpose |
|---|---|
| `users_user` | Stores application users and authentication-related user data. |
| `finance_account` | Stores wallets, bank accounts, and e-wallets. |
| `finance_category` | Stores income and expense categories, including parent-child hierarchy. |
| `finance_transaction` | Stores income, expense, and transfer records in a unified transaction table. |
| `finance_budget` | Stores category-based monthly budgets and alert thresholds. |
| `finance_financialgoal` | Stores saving goals and progress. |
| `finance_recurringtransaction` | Stores recurring income, expense, and transfer templates. |

### Why a Unified Transaction Table?

Instead of physically separating income and expenses into different tables, the application uses one table called `finance_transaction` with a `type` field.

This design:

- reduces repeated fields across income and expense records,
- supports income, expense, and transfer in one structure,
- makes financial reporting easier,
- allows filtering by user, account, category, transaction type, and date.

To remain compatible with the assignment requirement, the advanced SQL file also provides SQL views such as:

```text
Income
Expenses
ExpenseCategories
BankAccounts
```

These views expose the normalized implementation in a structure closer to the assignment specification.

---

## 6. SQL Deliverables

The `database/` folder contains all SQL-related submission files.

| File | Purpose |
|---|---|
| `01_create_database.sql` | Creates the MySQL database. |
| `02_schema.sql` | Full implemented schema exported from the Django/MySQL database. |
| `02b_schema_clean.sql` | Clean business-focused schema for SQL evaluation, excluding Django internal framework tables. |
| `03_sample_data.sql` | Inserts representative sample data. |
| `04_queries.sql` | Contains analytical SQL queries for financial reporting. |
| `05_advanced_objects.sql` | Optional advanced SQL objects: indexes, views, stored procedures, user-defined functions, and triggers. |
| `06_security_roles.sql` | Optional database security and administration script using MySQL roles and GRANT/REVOKE examples. |
| `README_SQL_FILES.md` | Explains the purpose and safe usage of SQL files. |

### ⚠️ Important Trigger Warning

`05_advanced_objects.sql` contains optional trigger examples for automatic balance updates at the database layer.

The Django application already updates account balances using Python application logic. Therefore, the trigger section should **not** be enabled together with the Django balance update logic unless the Python balance update logic is disabled. Otherwise, account balances may be updated twice.

---

## 7. SQL Query Highlights

The improved `04_queries.sql` demonstrates stronger SQL usage, including:

- user-specific filtering using `WHERE user_id = @target_user_id`,
- monthly income, expense, and net cashflow reporting,
- `CASE WHEN` logic for conditional aggregation,
- `LEFT JOIN` and `COALESCE` for budget-versus-spent calculations,
- Common Table Expressions (CTEs),
- Recursive CTE for parent-child category hierarchy,
- window functions such as `LAG()`, `SUM() OVER()`, and `RANK()`,
- goal progress and recurring transaction monitoring.

---

## 8. Local Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/tunglam021006-lgtm/SQL_final_prj.git
cd SQL_final_prj
```

If your local folder name is different, open the folder that contains `manage.py`.

### Step 2: Create and Activate Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Then edit `.env` with your local MySQL settings:

```env
SECRET_KEY=django-insecure-change-this-for-local-dev
DEBUG=True

DB_NAME=personal_finance_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

> Do not upload your real `.env` file to GitHub.

### Step 5: Create MySQL Database

Log in to MySQL and create the database:

```sql
CREATE DATABASE personal_finance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Alternatively, run:

```bash
mysql -u root -p < database/01_create_database.sql
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create a Superuser Optional

```bash
python manage.py createsuperuser
```

### Step 8: Seed May 2026 Demo Data Optional

The project includes a Django management command that creates diverse demo data for May 2026.

```bash
python manage.py seed_may_demo --reset
```

This command creates or updates sample wallets, categories, budgets, goals, recurring transactions, and **42 transactions** for the demo user.

Default demo username:

```text
taikhoantest
```

If the user does not exist, the seed command creates it for local demonstration. Change any demo password before using the system outside local testing.

### Step 9: Run the Development Server

```bash
python manage.py runserver
```

Open the website:

```text
http://127.0.0.1:8000/
```

---

## 9. Useful Development Commands

| Task | Command |
|---|---|
| Check Django project | `python manage.py check` |
| Apply migrations | `python manage.py migrate` |
| Run server | `python manage.py runserver` |
| Seed demo data | `python manage.py seed_may_demo --reset` |
| Run SQL queries manually | `mysql -u root -p personal_finance_db < database/04_queries.sql` |

---

## 10. Demo Data Summary

The May 2026 demo dataset includes:

- multiple wallets/accounts,
- income categories and expense categories,
- parent-child category hierarchy,
- monthly budgets,
- financial goals,
- recurring transaction templates,
- 42 financial transactions covering income, expenses, and transfers.

This data supports dashboard charts, category spending reports, budget alerts, transaction history, goal progress, and recurring transaction demonstrations.

---

## 11. Testing and Validation

The project was tested for:

- registration, login, and logout,
- wallet creation and deletion,
- category creation and hierarchy display,
- income, expense, and transfer transactions,
- automatic account balance updates,
- transaction deletion and balance recalculation,
- budget spent, remaining, usage percentage, and status calculation,
- parent and child category spending aggregation,
- financial goal progress calculation,
- recurring transaction creation and manual application,
- English/Vietnamese language toggle,
- SQL query reporting consistency.

---

## 12. Known Limitations

- The application is designed for local academic demonstration.
- It does not connect to real bank APIs.
- It does not process real payment transactions.
- Production deployment, automated backups, and advanced access control are future improvements.
- Optional SQL triggers should not be enabled together with Django balance update logic unless the Python balance update logic is disabled.

---

## 13. Future Improvements

- Add richer transaction search and export features.
- Add predictive budgeting suggestions.
- Add Docker deployment.
- Add cloud deployment instructions.
- Improve database backup and recovery automation.
- Expand security roles and access control.
- Further test stored procedures and triggers in a separate database environment.

---

## 14. Submission Links

| Item | Link |
|---|---|
| GitHub Repository | https://github.com/tunglam021006-lgtm/SQL_final_prj |
| YouTube Presentation | https://youtu.be/I92ByVNMSEs |

---

## 15. References

- Django Documentation: https://docs.djangoproject.com/
- MySQL 8.0 Reference Manual: https://dev.mysql.com/doc/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- ERDPlus: https://erdplus.com/
- MySQL Workbench Manual: https://dev.mysql.com/doc/workbench/en/
- Python Documentation: https://docs.python.org/
- GitHub Docs: https://docs.github.com/

---

<div align="center">

### ✅ Project 13 – Personal Finance Management System

**Relational database design + SQL scripting + Django web application**

</div>
