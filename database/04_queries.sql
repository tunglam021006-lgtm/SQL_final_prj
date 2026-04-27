USE personal_finance_db;

-- 1. Total income by month
SELECT
    YEAR(occurred_at) AS year,
    MONTH(occurred_at) AS month,
    SUM(amount) AS total_income
FROM finance_transaction
WHERE type = 'income'
GROUP BY YEAR(occurred_at), MONTH(occurred_at)
ORDER BY year, month;

-- 2. Total expense by month
SELECT
    YEAR(occurred_at) AS year,
    MONTH(occurred_at) AS month,
    SUM(amount) AS total_expense
FROM finance_transaction
WHERE type = 'expense'
GROUP BY YEAR(occurred_at), MONTH(occurred_at)
ORDER BY year, month;

-- 3. Net cashflow by month
SELECT
    YEAR(occurred_at) AS year,
    MONTH(occurred_at) AS month,
    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense,
    SUM(CASE WHEN type = 'income' THEN amount WHEN type = 'expense' THEN -amount ELSE 0 END) AS net_cashflow
FROM finance_transaction
GROUP BY YEAR(occurred_at), MONTH(occurred_at)
ORDER BY year, month;

-- 4. Expense by category in current month
SELECT
    c.name AS category_name,
    SUM(t.amount) AS total_spent
FROM finance_transaction t
JOIN finance_category c ON t.category_id = c.id
WHERE t.type = 'expense'
  AND MONTH(t.occurred_at) = MONTH(CURDATE())
  AND YEAR(t.occurred_at) = YEAR(CURDATE())
GROUP BY c.name
ORDER BY total_spent DESC;

-- 5. Top 5 largest expenses
SELECT
    t.id,
    t.amount,
    c.name AS category_name,
    a.name AS account_name,
    t.notes,
    t.occurred_at
FROM finance_transaction t
LEFT JOIN finance_category c ON t.category_id = c.id
JOIN finance_account a ON t.account_id = a.id
WHERE t.type = 'expense'
ORDER BY t.amount DESC
LIMIT 5;

-- 6. Wallet balances
SELECT
    id,
    name,
    type,
    currency,
    initial_balance,
    balance
FROM finance_account
WHERE is_active = 1
ORDER BY balance DESC;

-- 7. Recent 10 transactions
SELECT
    t.id,
    t.type,
    t.amount,
    c.name AS category_name,
    a.name AS source_account,
    da.name AS destination_account,
    t.notes,
    t.occurred_at
FROM finance_transaction t
LEFT JOIN finance_category c ON t.category_id = c.id
JOIN finance_account a ON t.account_id = a.id
LEFT JOIN finance_account da ON t.destination_account_id = da.id
ORDER BY t.occurred_at DESC
LIMIT 10;

-- 8. Budget vs spent
SELECT
    b.id,
    c.name AS category_name,
    b.amount AS budget_amount,
    COALESCE(SUM(t.amount), 0) AS spent_amount,
    b.amount - COALESCE(SUM(t.amount), 0) AS remaining_amount,
    ROUND(COALESCE(SUM(t.amount), 0) / b.amount * 100, 2) AS usage_percent,
    b.month,
    b.year
FROM finance_budget b
JOIN finance_category c ON b.category_id = c.id
LEFT JOIN finance_transaction t
    ON t.category_id = b.category_id
   AND t.type = 'expense'
   AND MONTH(t.occurred_at) = b.month
   AND YEAR(t.occurred_at) = b.year
GROUP BY b.id, c.name, b.amount, b.month, b.year
ORDER BY b.year DESC, b.month DESC, c.name;

-- 9. Financial goals progress
SELECT
    id,
    name,
    target_amount,
    current_amount,
    (target_amount - current_amount) AS remaining_amount,
    ROUND(current_amount / target_amount * 100, 2) AS progress_percent,
    deadline
FROM finance_financialgoal
WHERE is_active = 1
ORDER BY deadline, created_at DESC;

-- 10. Recurring transactions due in next 7 days
SELECT
    id,
    title,
    type,
    amount,
    frequency,
    next_due_date,
    auto_create
FROM finance_recurringtransaction
WHERE is_active = 1
  AND next_due_date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
ORDER BY next_due_date ASC;