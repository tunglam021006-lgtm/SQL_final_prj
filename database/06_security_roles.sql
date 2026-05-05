USE personal_finance_db;

-- ============================================================
-- 06_security_roles.sql
-- Optional MySQL security and administration script.
-- Replace passwords before running in a real environment.
-- ============================================================

CREATE ROLE IF NOT EXISTS 'finance_readonly';
CREATE ROLE IF NOT EXISTS 'finance_app_user';
CREATE ROLE IF NOT EXISTS 'finance_admin_role';

-- Read-only role: can inspect reports but cannot modify data.
GRANT SELECT ON personal_finance_db.* TO 'finance_readonly';

-- Application role: can operate on business tables used by the web app.
GRANT SELECT, INSERT, UPDATE, DELETE ON personal_finance_db.users_user TO 'finance_app_user';
GRANT SELECT, INSERT, UPDATE, DELETE ON personal_finance_db.finance_account TO 'finance_app_user';
GRANT SELECT, INSERT, UPDATE, DELETE ON personal_finance_db.finance_category TO 'finance_app_user';
GRANT SELECT, INSERT, UPDATE, DELETE ON personal_finance_db.finance_transaction TO 'finance_app_user';
GRANT SELECT, INSERT, UPDATE, DELETE ON personal_finance_db.finance_budget TO 'finance_app_user';
GRANT SELECT, INSERT, UPDATE, DELETE ON personal_finance_db.finance_financialgoal TO 'finance_app_user';
GRANT SELECT, INSERT, UPDATE, DELETE ON personal_finance_db.finance_recurringtransaction TO 'finance_app_user';

-- Admin role: full privileges for database maintenance.
GRANT ALL PRIVILEGES ON personal_finance_db.* TO 'finance_admin_role';

-- Example users. Change passwords before use.
CREATE USER IF NOT EXISTS 'finance_viewer'@'localhost' IDENTIFIED BY 'ChangeThisReadonlyPassword!';
CREATE USER IF NOT EXISTS 'finance_app'@'localhost' IDENTIFIED BY 'ChangeThisAppPassword!';

GRANT 'finance_readonly' TO 'finance_viewer'@'localhost';
GRANT 'finance_app_user' TO 'finance_app'@'localhost';

SET DEFAULT ROLE 'finance_readonly' TO 'finance_viewer'@'localhost';
SET DEFAULT ROLE 'finance_app_user' TO 'finance_app'@'localhost';

-- Example revoke command for demonstration:
-- REVOKE DELETE ON personal_finance_db.finance_transaction FROM 'finance_app_user';

FLUSH PRIVILEGES;
