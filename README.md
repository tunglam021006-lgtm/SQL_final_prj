# 💸 Personal Finance Management Web Application

<div align="center">

![Django](https://img.shields.io/badge/Backend-Django-0C4B33?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Language](https://img.shields.io/badge/Language-English%20%7C%20Vietnamese-ff69b4?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Course%20Project-success?style=for-the-badge)

**A bilingual web-based personal finance management system built with Django, MySQL, and Bootstrap.**

✨ Track your money • 📊 Understand your spending • 🎯 Reach your goals

</div>

---

## 🌟 Project Overview

This project is a **personal finance management web application** developed for academic purposes.

It helps users:

- 💼 manage multiple wallets and accounts  
- 💸 record income, expenses, and transfers  
- 🗂️ organize transactions using categories  
- 📉 track budgets by category  
- 🎯 create and monitor financial goals  
- 🔁 manage recurring transactions  
- 📊 view useful analytics on a dashboard  
- 🌐 switch between **English** and **Vietnamese**

> **Goal:** make personal finance tracking more practical, clear, and user-friendly through a clean dashboard-based interface.

---

## 🧩 Key Features

### 📊 1. Dashboard
- monthly income, expense, and net savings overview
- total wallet balance summary
- recent transactions
- budget alerts
- top spending categories
- goals overview
- recurring transactions due soon

### 👛 2. Wallet / Account Management
- support for **cash wallets**
- support for **bank accounts**
- support for **e-wallets**
- current balance tracking
- initial balance storage

### 🧾 3. Transaction Management
- add income transactions
- add expense transactions
- add transfer transactions
- automatic wallet balance updates
- transaction filtering and sorting
- recent history display

### 🏷️ 4. Category Management
- create income categories
- create expense categories
- support parent-child category structure

### 📌 5. Budget Management
- assign budgets by category
- monitor actual spending
- budget usage percentage
- alert threshold support

### 🎯 6. Financial Goals
- create savings goals
- update goal progress
- track target amount, current amount, and remaining amount
- completion status

### 🔁 7. Recurring Transactions
- repeating income
- repeating expenses
- repeating transfers
- next due date tracking
- manual apply action for recurring items

### 🌐 8. Bilingual Interface
- English and Vietnamese language toggle
- more accessible and user-friendly interface

---

## 🛠️ Technology Stack

| Layer | Technology |
|------|------------|
| **Backend** | Django |
| **Database** | MySQL |
| **Frontend** | HTML, CSS, Bootstrap, JavaScript |
| **ORM** | Django ORM |

---

## 🧱 System Architecture

```text
User Interface
    ↓
Django Views / Templates
    ↓
Django ORM
    ↓
MySQL Database
```

### 🔄 Request Flow
1. the user interacts with the web interface  
2. Django receives and processes the request  
3. Django ORM translates application logic into SQL queries  
4. MySQL stores or returns the requested data  
5. Django renders the updated result back to the browser  

---

## 📁 Project Structure

```text
Project-13-Personal-Finance/
├── apps/
│   ├── finance/              # core finance models and admin
│   ├── users/                # user model and authentication logic
│   └── web/                  # views, templates, routes, UI logic
├── config/                   # project settings, urls, UI texts
├── database/
│   ├── 01_create_database.sql
│   ├── 02_schema.sql
│   ├── 03_sample_data.sql
│   └── 04_queries.sql
├── manage.py
├── requirements.txt
└── README.md
```

---

## ✅ Prerequisites

Before running the project, make sure the following are installed:

- 🐍 **Python 3.11**
- 🐬 **MySQL Server 8.x**
- 📦 **pip**

Optional but recommended:
- 🧰 **MySQL Workbench**
- 🌿 **Git**

---

## 🚀 Installation Guide

### 1. Clone or download the project

```bash
git clone <your-repository-url>
cd Project-13-Personal-Finance
```

If the project is submitted as a ZIP file, simply extract it and open a terminal inside the project folder.

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

#### Windows
```bash
venv\Scripts\activate
```

#### macOS / Linux
```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing or incomplete, install the main packages manually:

```bash
pip install django mysqlclient djangorestframework
```

---

## 🗄️ Database Setup

The project uses **MySQL**.

### Step 1: Create the database
Run:

```sql
database/01_create_database.sql
```

This creates the database:

```sql
personal_finance_db
```

### Step 2: Import the schema
Run:

```sql
database/02_schema.sql
```

This creates all required tables.

### Step 3: Import the sample data
Run:

```sql
database/03_sample_data.sql
```

This inserts sample/demo records for testing.

---

## ▶️ Running the Application

### 1. Configure database settings

Open:

```text
config/settings.py
```

Find the `DATABASES` section and update it to match the MySQL setup on your machine.

Example:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "personal_finance_db",
        "USER": "root",
        "PASSWORD": "your_mysql_password",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

---

### 2. Apply migrations if needed

```bash
python manage.py migrate
```

---

### 3. Run the development server

```bash
python manage.py runserver
```

Open the browser and go to:

```text
http://127.0.0.1:8000/
```

---

## 🧪 Demo Data

If the sample data is imported successfully, the application can be tested immediately.

You may also reset a demo password if needed:

```bash
python manage.py changepassword taikhoantest
```

Or create a new superuser:

```bash
python manage.py createsuperuser
```

---

## 🧠 SQL Files Included

### `01_create_database.sql`
Creates the MySQL database.

### `02_schema.sql`
Contains the full database schema:
- table definitions
- constraints
- foreign keys
- indexes

### `03_sample_data.sql`
Contains demo/sample data for:
- users
- accounts
- categories
- budgets
- financial goals
- recurring transactions
- transactions

### `04_queries.sql`
Contains analytical SQL queries used for:
- monthly income analysis
- monthly expense analysis
- net cashflow calculation
- spending by category
- wallet balance overview
- recent transaction review
- budget versus actual spending comparison
- financial goal progress tracking
- recurring transaction monitoring

---

## 🔗 How the Website Connects to SQL

The website does **not** directly use the `.sql` files during normal runtime.

Instead:

- the `.sql` files are used to **create**, **restore**, and **demonstrate** the database
- the running web application connects to **MySQL** through **Django ORM**
- Django automatically generates SQL queries behind the scenes based on models and views

### In simple terms

- 📄 `.sql` files = database setup and demonstration artifacts  
- ⚙️ Django ORM = the layer that actually communicates with MySQL while the website is running  

This means:

- `02_schema.sql` recreates the table structure
- `03_sample_data.sql` restores demo data
- `04_queries.sql` demonstrates the SQL/database part of the project
- the website itself reads and writes data through Django models

---

## ✅ Testing Checklist

Before submission, it is recommended to test the following:

### Authentication
- [ ] login page loads correctly
- [ ] user can log in
- [ ] user can log out

### Dashboard
- [ ] dashboard loads without error
- [ ] income/expense summaries display correctly
- [ ] charts and summary cards appear correctly

### Wallets
- [ ] create wallet
- [ ] delete wallet
- [ ] current balance displays correctly

### Categories
- [ ] create income category
- [ ] create expense category
- [ ] create child category
- [ ] delete category

### Transactions
- [ ] create income transaction
- [ ] create expense transaction
- [ ] create transfer transaction
- [ ] delete transaction
- [ ] balances update automatically

### Budgets
- [ ] create budget
- [ ] usage percentage updates correctly
- [ ] delete budget

### Goals
- [ ] create goal
- [ ] update goal progress
- [ ] delete goal

### Recurring Transactions
- [ ] create recurring income
- [ ] create recurring expense
- [ ] create recurring transfer
- [ ] apply recurring item manually
- [ ] delete recurring item

### Language Toggle
- [ ] English mode works
- [ ] Vietnamese mode works
- [ ] main pages remain readable in both languages

---

## 🧯 Troubleshooting

### Problem: database connection error
Check:
- MySQL server is running
- database name is correct
- MySQL username and password in `settings.py` are correct

### Problem: missing Python package
Run:

```bash
pip install -r requirements.txt
```

### Problem: imported user cannot log in
Reset the password:

```bash
python manage.py changepassword taikhoantest
```

### Problem: tables not found
Make sure:
- `01_create_database.sql` was executed
- `02_schema.sql` was imported successfully
- the correct database name is set in `config/settings.py`

### Problem: server does not start after editing Python files
Check for:
- indentation errors in Python
- missing commas or brackets
- invalid import statements

---

## 🚧 Future Improvements

Possible extensions for the system include:

- richer filtering and search for transactions
- export to Excel or PDF
- recurring transaction automation scheduler
- better data validation and suggestions
- improved analytics and visualizations
- user profile settings
- mobile optimization
- Docker deployment
- cloud deployment

---

## 📝 Notes

- This project was created for academic and demonstration purposes.
- Sample data is included to make testing and evaluation easier.
- The interface supports both **English** and **Vietnamese**.
- The project uses **Django ORM** for runtime database interaction, while SQL scripts are included for setup and evaluation.
- If the project is shared with another user or instructor, they must configure MySQL locally before running the web application.

---

## 👤 Author

**Personal Finance Management Web Application**  
Course project submission

---

<div align="center">

### ✨ Thanks for visiting this project!

💡 If you upload this to GitHub, this decorated version will look much nicer and easier to read.

</div>
