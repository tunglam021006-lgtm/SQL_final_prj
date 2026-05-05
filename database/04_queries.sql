USE personal_finance_db;

-- ============================================================
-- 04_queries.sql
-- Analytical SQL queries for Personal Finance Management System
-- All queries are scoped by @target_user_id to protect user data.
-- Change this variable to test another user.
-- ============================================================
SET @target_user_id := 1;

-- 1. Monthly financial summary: income, expenses, transfers, and net cashflow
SELECT
    YEAR(t.occurred_at) AS report_year,
    MONTH(t.occurred_at) AS report_month,
    SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END) AS total_income,
    SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END) AS total_expense,
    SUM(CASE WHEN t.type = 'transfer' THEN t.amount ELSE 0 END) AS total_transfer_volume,
    SUM(CASE
        WHEN t.type = 'income' THEN t.amount
        WHEN t.type = 'expense' THEN -t.amount
        ELSE 0
    END) AS net_cashflow
FROM finance_transaction t
WHERE t.user_id = @target_user_id
GROUP BY YEAR(t.occurred_at), MONTH(t.occurred_at)
ORDER BY report_year, report_month;

-- 2. Monthly cashflow trend with window function LAG()
-- Shows how net cashflow changes from the previous month.
WITH monthly_cashflow AS (
    SELECT
        YEAR(t.occurred_at) AS report_year,
        MONTH(t.occurred_at) AS report_month,
        SUM(CASE
            WHEN t.type = 'income' THEN t.amount
            WHEN t.type = 'expense' THEN -t.amount
            ELSE 0
        END) AS net_cashflow
    FROM finance_transaction t
    WHERE t.user_id = @target_user_id
    GROUP BY YEAR(t.occurred_at), MONTH(t.occurred_at)
)
SELECT
    report_year,
    report_month,
    net_cashflow,
    LAG(net_cashflow) OVER (ORDER BY report_year, report_month) AS previous_month_net_cashflow,
    net_cashflow - LAG(net_cashflow) OVER (ORDER BY report_year, report_month) AS month_to_month_change
FROM monthly_cashflow
ORDER BY report_year, report_month;

-- 3. Running net cashflow by transaction using SUM() OVER()
-- Transfers are ignored for net cashflow because they move money between owned accounts.
SELECT
    t.id,
    t.occurred_at,
    t.type,
    t.amount,
    a.name AS source_account,
    c.name AS category_name,
    SUM(CASE
        WHEN t.type = 'income' THEN t.amount
        WHEN t.type = 'expense' THEN -t.amount
        ELSE 0
    END) OVER (ORDER BY t.occurred_at, t.id) AS running_net_cashflow
FROM finance_transaction t
JOIN finance_account a ON t.account_id = a.id
LEFT JOIN finance_category c ON t.category_id = c.id
WHERE t.user_id = @target_user_id
ORDER BY t.occurred_at, t.id;

-- 4. Top expense categories in the current month with RANK()
SELECT
    c.name AS category_name,
    SUM(t.amount) AS total_spent,
    RANK() OVER (ORDER BY SUM(t.amount) DESC) AS spending_rank
FROM finance_transaction t
JOIN finance_category c ON t.category_id = c.id
WHERE t.user_id = @target_user_id
  AND t.type = 'expense'
  AND YEAR(t.occurred_at) = YEAR(CURDATE())
  AND MONTH(t.occurred_at) = MONTH(CURDATE())
GROUP BY c.id, c.name
ORDER BY spending_rank, category_name;

-- 5. Recursive CTE: category tree and spending by parent category
-- Useful because finance_category supports parent_id for subcategories.
WITH RECURSIVE category_tree AS (
    SELECT
        c.id AS root_category_id,
        c.id AS category_id,
        c.name AS root_category_name,
        c.name AS category_name,
        0 AS depth
    FROM finance_category c
    WHERE c.user_id = @target_user_id
      AND c.type = 'expense'
      AND c.parent_id IS NULL
      AND c.is_active = 1

    UNION ALL

    SELECT
        ct.root_category_id,
        child.id AS category_id,
        ct.root_category_name,
        child.name AS category_name,
        ct.depth + 1 AS depth
    FROM category_tree ct
    JOIN finance_category child ON child.parent_id = ct.category_id
    WHERE child.user_id = @target_user_id
      AND child.type = 'expense'
      AND child.is_active = 1
)
SELECT
    ct.root_category_name AS parent_category,
    COALESCE(SUM(t.amount), 0) AS total_spent_including_children
FROM category_tree ct
LEFT JOIN finance_transaction t
    ON t.category_id = ct.category_id
   AND t.user_id = @target_user_id
   AND t.type = 'expense'
   AND YEAR(t.occurred_at) = YEAR(CURDATE())
   AND MONTH(t.occurred_at) = MONTH(CURDATE())
GROUP BY ct.root_category_id, ct.root_category_name
ORDER BY total_spent_including_children DESC;

-- 6. Budget vs spent, including spending from child categories
WITH RECURSIVE budget_category_tree AS (
    SELECT
        b.id AS budget_id,
        b.user_id,
        b.category_id AS root_category_id,
        b.category_id AS category_id,
        b.amount AS budget_amount,
        b.month,
        b.year,
        b.alert_threshold
    FROM finance_budget b
    WHERE b.user_id = @target_user_id

    UNION ALL

    SELECT
        bct.budget_id,
        bct.user_id,
        bct.root_category_id,
        child.id AS category_id,
        bct.budget_amount,
        bct.month,
        bct.year,
        bct.alert_threshold
    FROM budget_category_tree bct
    JOIN finance_category child ON child.parent_id = bct.category_id
    WHERE child.user_id = @target_user_id
      AND child.is_active = 1
)
SELECT
    bct.budget_id,
    root_cat.name AS category_name,
    bct.budget_amount,
    COALESCE(SUM(t.amount), 0) AS spent_amount,
    bct.budget_amount - COALESCE(SUM(t.amount), 0) AS remaining_amount,
    ROUND(COALESCE(SUM(t.amount), 0) / NULLIF(bct.budget_amount, 0) * 100, 2) AS usage_percent,
    CASE
        WHEN COALESCE(SUM(t.amount), 0) >= bct.budget_amount THEN 'Over'
        WHEN ROUND(COALESCE(SUM(t.amount), 0) / NULLIF(bct.budget_amount, 0) * 100, 2) >= bct.alert_threshold THEN 'Warning'
        ELSE 'Safe'
    END AS budget_status,
    bct.month,
    bct.year
FROM budget_category_tree bct
JOIN finance_category root_cat ON root_cat.id = bct.root_category_id
LEFT JOIN finance_transaction t
    ON t.user_id = @target_user_id
   AND t.type = 'expense'
   AND t.category_id = bct.category_id
   AND MONTH(t.occurred_at) = bct.month
   AND YEAR(t.occurred_at) = bct.year
GROUP BY
    bct.budget_id,
    root_cat.name,
    bct.budget_amount,
    bct.alert_threshold,
    bct.month,
    bct.year
ORDER BY bct.year DESC, bct.month DESC, usage_percent DESC;

-- 7. Wallet balances with ranking and percentage of total balance
SELECT
    a.id,
    a.name,
    a.type,
    a.currency,
    a.initial_balance,
    a.balance,
    RANK() OVER (ORDER BY a.balance DESC) AS balance_rank,
    ROUND(a.balance / NULLIF(SUM(a.balance) OVER (), 0) * 100, 2) AS percent_of_total_balance
FROM finance_account a
WHERE a.user_id = @target_user_id
  AND a.is_active = 1
ORDER BY balance_rank, a.name;

-- 8. Recent 10 transactions with readable account/category names
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
WHERE t.user_id = @target_user_id
ORDER BY t.occurred_at DESC, t.id DESC
LIMIT 10;

-- 9. Financial goal progress with calculated status
SELECT
    g.id,
    g.name,
    g.target_amount,
    g.current_amount,
    (g.target_amount - g.current_amount) AS remaining_amount,
    ROUND(g.current_amount / NULLIF(g.target_amount, 0) * 100, 2) AS progress_percent,
    CASE
        WHEN g.current_amount >= g.target_amount THEN 'Completed'
        WHEN g.deadline IS NOT NULL AND g.deadline < CURDATE() THEN 'Overdue'
        ELSE 'In progress'
    END AS goal_status,
    g.deadline
FROM finance_financialgoal g
WHERE g.user_id = @target_user_id
  AND g.is_active = 1
ORDER BY g.deadline, g.created_at DESC;

-- 10. Recurring transactions due in the next 7 days
SELECT
    r.id,
    r.title,
    r.type,
    r.amount,
    a.name AS source_account,
    da.name AS destination_account,
    c.name AS category_name,
    r.frequency,
    r.next_due_date,
    DATEDIFF(r.next_due_date, CURDATE()) AS days_until_due,
    r.auto_create
FROM finance_recurringtransaction r
JOIN finance_account a ON r.account_id = a.id
LEFT JOIN finance_account da ON r.destination_account_id = da.id
LEFT JOIN finance_category c ON r.category_id = c.id
WHERE r.user_id = @target_user_id
  AND r.is_active = 1
  AND r.next_due_date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
ORDER BY r.next_due_date ASC, r.id ASC;
