-- ============================================================
-- 02b_schema_clean.sql
-- Clean business-focused schema for Personal Finance Management System
-- This file intentionally excludes Django internal tables such as
-- django_migrations, django_session, auth_group, and django_admin_log.
-- Use Django migrations for running the full web app; use this file to
-- present the core database design clearly for SQL evaluation.
-- ============================================================

CREATE DATABASE IF NOT EXISTS personal_finance_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE personal_finance_db;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS finance_recurringtransaction;
DROP TABLE IF EXISTS finance_financialgoal;
DROP TABLE IF EXISTS finance_budget;
DROP TABLE IF EXISTS finance_transaction;
DROP TABLE IF EXISTS finance_category;
DROP TABLE IF EXISTS finance_account;
DROP TABLE IF EXISTS users_user;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE users_user (
    id BIGINT NOT NULL AUTO_INCREMENT,
    username VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    password VARCHAR(128) NOT NULL,
    display_name VARCHAR(100) NULL,
    phone_number VARCHAR(20) NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    is_staff TINYINT(1) NOT NULL DEFAULT 0,
    is_superuser TINYINT(1) NOT NULL DEFAULT 0,
    date_joined DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    last_login DATETIME(6) NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE finance_account (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    bank_name VARCHAR(100) NULL,
    type VARCHAR(20) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'VND',
    initial_balance DECIMAL(15,0) NOT NULL DEFAULT 0,
    balance DECIMAL(15,0) NOT NULL DEFAULT 0,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    CONSTRAINT fk_account_user FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    CONSTRAINT chk_account_type CHECK (type IN ('cash', 'bank', 'e-wallet')),
    CONSTRAINT chk_account_initial_balance CHECK (initial_balance >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE finance_category (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    parent_id BIGINT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    CONSTRAINT fk_category_user FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) REFERENCES finance_category(id) ON DELETE CASCADE,
    CONSTRAINT chk_category_type CHECK (type IN ('income', 'expense')),
    UNIQUE KEY uq_category_user_type_name_parent (user_id, type, name, parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE finance_transaction (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    destination_account_id BIGINT NULL,
    category_id BIGINT NULL,
    type VARCHAR(20) NOT NULL,
    amount DECIMAL(15,0) NOT NULL,
    notes LONGTEXT NULL,
    occurred_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    CONSTRAINT fk_transaction_user FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_transaction_account FOREIGN KEY (account_id) REFERENCES finance_account(id) ON DELETE RESTRICT,
    CONSTRAINT fk_transaction_destination_account FOREIGN KEY (destination_account_id) REFERENCES finance_account(id) ON DELETE SET NULL,
    CONSTRAINT fk_transaction_category FOREIGN KEY (category_id) REFERENCES finance_category(id) ON DELETE SET NULL,
    CONSTRAINT chk_transaction_type CHECK (type IN ('income', 'expense', 'transfer')),
    CONSTRAINT chk_transaction_amount CHECK (amount > 0),
    CONSTRAINT chk_transfer_destination CHECK (
        (type <> 'transfer') OR (destination_account_id IS NOT NULL AND destination_account_id <> account_id)
    ),
    CONSTRAINT chk_transfer_no_category CHECK ((type <> 'transfer') OR category_id IS NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE finance_budget (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    amount DECIMAL(15,0) NOT NULL,
    period VARCHAR(20) NOT NULL DEFAULT 'monthly',
    month SMALLINT UNSIGNED NOT NULL,
    year INT UNSIGNED NOT NULL,
    alert_threshold DECIMAL(5,2) NOT NULL DEFAULT 80.00,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    CONSTRAINT fk_budget_user FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_budget_category FOREIGN KEY (category_id) REFERENCES finance_category(id) ON DELETE CASCADE,
    CONSTRAINT chk_budget_amount CHECK (amount > 0),
    CONSTRAINT chk_budget_period CHECK (period IN ('weekly', 'monthly')),
    CONSTRAINT chk_budget_month CHECK (month BETWEEN 1 AND 12),
    CONSTRAINT chk_budget_year CHECK (year >= 2000),
    CONSTRAINT chk_budget_alert_threshold CHECK (alert_threshold BETWEEN 0 AND 100),
    UNIQUE KEY uq_budget_user_category_period (user_id, category_id, period, month, year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE finance_financialgoal (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    name VARCHAR(120) NOT NULL,
    target_amount DECIMAL(14,2) NOT NULL,
    current_amount DECIMAL(14,2) NOT NULL DEFAULT 0,
    deadline DATE NULL,
    notes LONGTEXT NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    CONSTRAINT fk_goal_user FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    CONSTRAINT chk_goal_target_amount CHECK (target_amount > 0),
    CONSTRAINT chk_goal_current_amount CHECK (current_amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE finance_recurringtransaction (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    destination_account_id BIGINT NULL,
    category_id BIGINT NULL,
    title VARCHAR(120) NOT NULL,
    type VARCHAR(10) NOT NULL,
    amount DECIMAL(14,0) NOT NULL,
    frequency VARCHAR(10) NOT NULL DEFAULT 'monthly',
    next_due_date DATE NOT NULL,
    auto_create TINYINT(1) NOT NULL DEFAULT 0,
    last_generated_at DATETIME(6) NULL,
    notes LONGTEXT NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    CONSTRAINT fk_recurring_user FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_recurring_account FOREIGN KEY (account_id) REFERENCES finance_account(id) ON DELETE RESTRICT,
    CONSTRAINT fk_recurring_destination_account FOREIGN KEY (destination_account_id) REFERENCES finance_account(id) ON DELETE SET NULL,
    CONSTRAINT fk_recurring_category FOREIGN KEY (category_id) REFERENCES finance_category(id) ON DELETE SET NULL,
    CONSTRAINT chk_recurring_type CHECK (type IN ('income', 'expense', 'transfer')),
    CONSTRAINT chk_recurring_frequency CHECK (frequency IN ('weekly', 'monthly')),
    CONSTRAINT chk_recurring_amount CHECK (amount > 0),
    CONSTRAINT chk_recurring_transfer_destination CHECK (
        (type <> 'transfer') OR (destination_account_id IS NOT NULL AND destination_account_id <> account_id)
    ),
    CONSTRAINT chk_recurring_transfer_no_category CHECK ((type <> 'transfer') OR category_id IS NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Composite indexes for common reporting paths.
CREATE INDEX idx_account_user_active ON finance_account(user_id, is_active);
CREATE INDEX idx_category_user_type_parent ON finance_category(user_id, type, parent_id, is_active);
CREATE INDEX idx_transaction_user_date_type ON finance_transaction(user_id, occurred_at, type);
CREATE INDEX idx_transaction_user_category_date ON finance_transaction(user_id, category_id, occurred_at);
CREATE INDEX idx_budget_user_period_category ON finance_budget(user_id, year, month, category_id);
CREATE INDEX idx_recurring_user_active_due ON finance_recurringtransaction(user_id, is_active, next_due_date);
