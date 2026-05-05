# Database SQL Files Guide

This folder contains the SQL deliverables for Project 13 - Personal Finance Management System.

## Required / core files

- `01_create_database.sql`: creates the MySQL database.
- `02_schema.sql`: full schema export from the Django/MySQL database, including Django framework tables. This file is closest to the actual running application database.
- `03_sample_data.sql`: sample/demo data used by the application.
- `04_queries.sql`: analytical SQL queries for reporting and validation. All queries are scoped by `@target_user_id`.

## Additional SQL-evaluation files

- `02b_schema_clean.sql`: clean business-focused schema containing only the project tables. This is easier for evaluation than the full Django dump.
- `05_advanced_objects.sql`: optional advanced SQL objects: composite indexes, views, stored procedures, user-defined functions, and triggers.
- `06_security_roles.sql`: optional database security and administration script using MySQL roles and GRANT/REVOKE examples.

## Important warning about triggers

The Django web application already updates account balances in Python when transactions are created or deleted. Therefore, do **not** enable the balance triggers in `05_advanced_objects.sql` while also using the unmodified Django application, otherwise account balances may be updated twice.

Use `05_advanced_objects.sql` as a database-level alternative/demonstration for SQL evaluation, or disable the Python balance-update logic before using those triggers in the live application.
