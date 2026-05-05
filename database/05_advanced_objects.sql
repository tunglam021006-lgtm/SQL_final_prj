USE personal_finance_db;

-- ============================================================
-- 05_advanced_objects.sql
-- Optional advanced SQL objects for Personal Finance Management System
-- Includes: composite indexes, assignment-compatible views, reporting views,
-- stored functions, stored procedures, and triggers.
--
-- IMPORTANT:
-- The Django application already updates account balances in Python.
-- If the triggers in this file are installed and the Django app is used
-- without changing the Python balance-update logic, account balances may be
-- updated twice. Treat the trigger section as a database-level alternative
-- for SQL evaluation, or disable Python balance updates before using triggers
-- in the live web app.
-- ============================================================

-- ------------------------------------------------------------
-- 1. Composite indexes for common reporting paths
-- ------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_create_index_if_missing;
DELIMITER //
CREATE PROCEDURE sp_create_index_if_missing(
    IN p_table_name VARCHAR(128),
    IN p_index_name VARCHAR(128),
    IN p_create_sql TEXT
)
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.statistics
        WHERE table_schema = DATABASE()
          AND table_name = p_table_name
          AND index_name = p_index_name
    ) THEN
        SET @ddl_sql = p_create_sql;
        PREPARE stmt FROM @ddl_sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END//
DELIMITER ;

CALL sp_create_index_if_missing(
    'finance_transaction',
    'idx_tx_user_type_date',
    'CREATE INDEX idx_tx_user_type_date ON finance_transaction(user_id, type, occurred_at)'
);
CALL sp_create_index_if_missing(
    'finance_transaction',
    'idx_tx_user_category_date',
    'CREATE INDEX idx_tx_user_category_date ON finance_transaction(user_id, category_id, occurred_at)'
);
CALL sp_create_index_if_missing(
    'finance_transaction',
    'idx_tx_account_date',
    'CREATE INDEX idx_tx_account_date ON finance_transaction(account_id, occurred_at)'
);
CALL sp_create_index_if_missing(
    'finance_budget',
    'idx_budget_user_year_month_category',
    'CREATE INDEX idx_budget_user_year_month_category ON finance_budget(user_id, year, month, category_id)'
);
CALL sp_create_index_if_missing(
    'finance_recurringtransaction',
    'idx_recurring_active_due_user',
    'CREATE INDEX idx_recurring_active_due_user ON finance_recurringtransaction(is_active, next_due_date, user_id)'
);

DROP PROCEDURE IF EXISTS sp_create_index_if_missing;

-- ------------------------------------------------------------
-- 2. Assignment-compatible views
-- These views expose the normalized implementation in the table shapes
-- required by the assignment brief: Income, Expenses, ExpenseCategories,
-- and BankAccounts. The physical implementation still uses finance_transaction.
-- ------------------------------------------------------------
DROP VIEW IF EXISTS Income;
CREATE VIEW Income AS
SELECT
    id AS IncomeID,
    user_id AS UserID,
    amount AS Amount,
    occurred_at AS IncomeDate,
    notes AS Description
FROM finance_transaction
WHERE type = 'income';

DROP VIEW IF EXISTS Expenses;
CREATE VIEW Expenses AS
SELECT
    id AS ExpenseID,
    user_id AS UserID,
    category_id AS CategoryID,
    amount AS Amount,
    occurred_at AS ExpenseDate,
    notes AS Description
FROM finance_transaction
WHERE type = 'expense';

DROP VIEW IF EXISTS ExpenseCategories;
CREATE VIEW ExpenseCategories AS
SELECT
    id AS CategoryID,
    name AS CategoryName,
    user_id AS UserID,
    parent_id AS ParentCategoryID
FROM finance_category
WHERE type = 'expense'
  AND is_active = 1;

DROP VIEW IF EXISTS BankAccounts;
CREATE VIEW BankAccounts AS
SELECT
    id AS AccountID,
    user_id AS UserID,
    COALESCE(bank_name, name) AS BankName,
    balance AS Balance
FROM finance_account
WHERE is_active = 1;

-- ------------------------------------------------------------
-- 3. Reporting views
-- ------------------------------------------------------------
DROP VIEW IF EXISTS vw_monthly_income_summary;
CREATE VIEW vw_monthly_income_summary AS
SELECT
    user_id,
    YEAR(occurred_at) AS report_year,
    MONTH(occurred_at) AS report_month,
    SUM(amount) AS total_income,
    COUNT(*) AS income_count
FROM finance_transaction
WHERE type = 'income'
GROUP BY user_id, YEAR(occurred_at), MONTH(occurred_at);

DROP VIEW IF EXISTS vw_monthly_expense_summary;
CREATE VIEW vw_monthly_expense_summary AS
SELECT
    user_id,
    YEAR(occurred_at) AS report_year,
    MONTH(occurred_at) AS report_month,
    SUM(amount) AS total_expense,
    COUNT(*) AS expense_count
FROM finance_transaction
WHERE type = 'expense'
GROUP BY user_id, YEAR(occurred_at), MONTH(occurred_at);

DROP VIEW IF EXISTS vw_category_spending;
CREATE VIEW vw_category_spending AS
SELECT
    t.user_id,
    c.id AS category_id,
    c.name AS category_name,
    YEAR(t.occurred_at) AS report_year,
    MONTH(t.occurred_at) AS report_month,
    SUM(t.amount) AS total_spent,
    COUNT(*) AS transaction_count
FROM finance_transaction t
JOIN finance_category c ON t.category_id = c.id
WHERE t.type = 'expense'
GROUP BY t.user_id, c.id, c.name, YEAR(t.occurred_at), MONTH(t.occurred_at);

DROP VIEW IF EXISTS vw_monthly_net_cashflow;
CREATE VIEW vw_monthly_net_cashflow AS
SELECT
    user_id,
    YEAR(occurred_at) AS report_year,
    MONTH(occurred_at) AS report_month,
    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense,
    SUM(CASE
        WHEN type = 'income' THEN amount
        WHEN type = 'expense' THEN -amount
        ELSE 0
    END) AS net_cashflow
FROM finance_transaction
GROUP BY user_id, YEAR(occurred_at), MONTH(occurred_at);

-- ------------------------------------------------------------
-- 4. Stored functions
-- ------------------------------------------------------------
DROP FUNCTION IF EXISTS fn_total_income;
DROP FUNCTION IF EXISTS fn_total_expense;
DROP FUNCTION IF EXISTS fn_budget_status;

DELIMITER //

CREATE FUNCTION fn_total_income(p_user_id BIGINT, p_month INT, p_year INT)
RETURNS DECIMAL(15,0)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_total DECIMAL(15,0);

    SELECT COALESCE(SUM(amount), 0)
    INTO v_total
    FROM finance_transaction
    WHERE user_id = p_user_id
      AND type = 'income'
      AND MONTH(occurred_at) = p_month
      AND YEAR(occurred_at) = p_year;

    RETURN v_total;
END//

CREATE FUNCTION fn_total_expense(p_user_id BIGINT, p_month INT, p_year INT)
RETURNS DECIMAL(15,0)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_total DECIMAL(15,0);

    SELECT COALESCE(SUM(amount), 0)
    INTO v_total
    FROM finance_transaction
    WHERE user_id = p_user_id
      AND type = 'expense'
      AND MONTH(occurred_at) = p_month
      AND YEAR(occurred_at) = p_year;

    RETURN v_total;
END//

CREATE FUNCTION fn_budget_status(p_budget_id BIGINT)
RETURNS VARCHAR(20)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_budget_amount DECIMAL(15,0);
    DECLARE v_spent DECIMAL(15,0);
    DECLARE v_threshold DECIMAL(5,2);
    DECLARE v_usage DECIMAL(8,2);

    SELECT
        b.amount,
        b.alert_threshold,
        COALESCE(SUM(t.amount), 0)
    INTO
        v_budget_amount,
        v_threshold,
        v_spent
    FROM finance_budget b
    LEFT JOIN finance_transaction t
        ON t.user_id = b.user_id
       AND t.category_id = b.category_id
       AND t.type = 'expense'
       AND MONTH(t.occurred_at) = b.month
       AND YEAR(t.occurred_at) = b.year
    WHERE b.id = p_budget_id
    GROUP BY b.id, b.amount, b.alert_threshold;

    IF v_budget_amount IS NULL OR v_budget_amount <= 0 THEN
        RETURN 'Unknown';
    END IF;

    SET v_usage = v_spent / v_budget_amount * 100;

    IF v_usage >= 100 THEN
        RETURN 'Over';
    ELSEIF v_usage >= v_threshold THEN
        RETURN 'Warning';
    ELSE
        RETURN 'Safe';
    END IF;
END//

-- ------------------------------------------------------------
-- 5. Stored procedures
-- These procedures insert transactions. Balance updates are handled by
-- the triggers below when the trigger section is enabled.
-- ------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_add_income_and_update_balance//
DROP PROCEDURE IF EXISTS sp_add_expense_and_update_balance//
DROP PROCEDURE IF EXISTS sp_monthly_close_summary//

CREATE PROCEDURE sp_add_income_and_update_balance(
    IN p_user_id BIGINT,
    IN p_account_id BIGINT,
    IN p_category_id BIGINT,
    IN p_amount DECIMAL(15,0),
    IN p_notes TEXT,
    IN p_occurred_at DATETIME(6)
)
BEGIN
    INSERT INTO finance_transaction
        (user_id, account_id, destination_account_id, category_id, type, amount, notes, occurred_at, created_at)
    VALUES
        (p_user_id, p_account_id, NULL, p_category_id, 'income', p_amount, p_notes, COALESCE(p_occurred_at, NOW(6)), NOW(6));
END//

CREATE PROCEDURE sp_add_expense_and_update_balance(
    IN p_user_id BIGINT,
    IN p_account_id BIGINT,
    IN p_category_id BIGINT,
    IN p_amount DECIMAL(15,0),
    IN p_notes TEXT,
    IN p_occurred_at DATETIME(6)
)
BEGIN
    INSERT INTO finance_transaction
        (user_id, account_id, destination_account_id, category_id, type, amount, notes, occurred_at, created_at)
    VALUES
        (p_user_id, p_account_id, NULL, p_category_id, 'expense', p_amount, p_notes, COALESCE(p_occurred_at, NOW(6)), NOW(6));
END//

CREATE PROCEDURE sp_monthly_close_summary(
    IN p_user_id BIGINT,
    IN p_month INT,
    IN p_year INT
)
BEGIN
    SELECT
        p_user_id AS user_id,
        p_year AS report_year,
        p_month AS report_month,
        fn_total_income(p_user_id, p_month, p_year) AS total_income,
        fn_total_expense(p_user_id, p_month, p_year) AS total_expense,
        fn_total_income(p_user_id, p_month, p_year) - fn_total_expense(p_user_id, p_month, p_year) AS net_cashflow;
END//

-- ------------------------------------------------------------
-- 6. Triggers
-- Do not enable these triggers together with Django's Python balance-update
-- logic unless the Python balance-update logic is disabled.
-- ------------------------------------------------------------
DROP TRIGGER IF EXISTS trg_transaction_after_insert_balance//
DROP TRIGGER IF EXISTS trg_transaction_after_delete_balance//

CREATE TRIGGER trg_transaction_after_insert_balance
AFTER INSERT ON finance_transaction
FOR EACH ROW
BEGIN
    IF NEW.type = 'income' THEN
        UPDATE finance_account
        SET balance = balance + NEW.amount
        WHERE id = NEW.account_id;
    ELSEIF NEW.type = 'expense' THEN
        UPDATE finance_account
        SET balance = balance - NEW.amount
        WHERE id = NEW.account_id;
    ELSEIF NEW.type = 'transfer' THEN
        UPDATE finance_account
        SET balance = balance - NEW.amount
        WHERE id = NEW.account_id;

        UPDATE finance_account
        SET balance = balance + NEW.amount
        WHERE id = NEW.destination_account_id;
    END IF;
END//

CREATE TRIGGER trg_transaction_after_delete_balance
AFTER DELETE ON finance_transaction
FOR EACH ROW
BEGIN
    IF OLD.type = 'income' THEN
        UPDATE finance_account
        SET balance = balance - OLD.amount
        WHERE id = OLD.account_id;
    ELSEIF OLD.type = 'expense' THEN
        UPDATE finance_account
        SET balance = balance + OLD.amount
        WHERE id = OLD.account_id;
    ELSEIF OLD.type = 'transfer' THEN
        UPDATE finance_account
        SET balance = balance + OLD.amount
        WHERE id = OLD.account_id;

        UPDATE finance_account
        SET balance = balance - OLD.amount
        WHERE id = OLD.destination_account_id;
    END IF;
END//

DELIMITER ;

-- ------------------------------------------------------------
-- 7. Quick checks after installation
-- ------------------------------------------------------------
SELECT 'Advanced objects installed. Remember: do not run Django balance updates and SQL triggers together.' AS note;
