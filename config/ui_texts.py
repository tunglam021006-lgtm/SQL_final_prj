SUPPORTED_LANGS = ("vi", "en")


UI_TEXTS = {
    "vi": {
        "app_name": "Expense Manager",
        "nav_dashboard": "Bảng điều khiển",
        "nav_transactions": "Giao dịch",
        "nav_wallets": "Ví tiền",
        "nav_categories": "Danh mục",
        "nav_budgets": "Ngân sách",
        "logout": "Đăng xuất",
        "quick_actions": "Tác vụ nhanh",
        "view_all_transactions": "Xem tất cả giao dịch",
        "manage_budgets": "Quản lý ngân sách",

        "dashboard_title": "Bảng điều khiển",
        "dashboard_overview": "Tổng quan tháng {month}/{year}",
        "total_income": "Tổng thu",
        "total_expense": "Tổng chi",
        "net_cashflow": "Dòng tiền ròng",
        "wallet_balance": "Số dư ví",
        "transactions_this_month": "Giao dịch tháng này",
        "largest_expense": "Khoản chi lớn nhất",
        "expense_categories_used": "Số danh mục chi dùng",
        "budget_risk": "Rủi ro ngân sách",
        "cashflow_trend": "Xu hướng dòng tiền",
        "expense_breakdown": "Cơ cấu chi tiêu",
        "budget_vs_spent": "Ngân sách và thực chi",
        "wallet_distribution": "Phân bổ số dư ví",
        "budget_alerts": "Cảnh báo ngân sách",
        "top_spending_categories": "Danh mục chi tiêu nhiều nhất",
        "recent_transactions": "Giao dịch gần đây",
        "see_all": "Xem tất cả",

        "quick_add_title": "Thêm nhanh",
        "quick_add_hint": "Nhập 1 dòng để lưu giao dịch nhanh.",
        "quick_add_examples": "Ví dụ: 45k cafe, 120k ăn trưa, 100k mua quần áo, 500k chuyển Momo",
        "quick_add_placeholder": "Ví dụ: 45k cafe hoặc 500k chuyển Momo",
        "save_fast": "Lưu nhanh",
        "one_tap_repeat": "Lặp lại nhanh",
        "recurring_suggestions": "Gợi ý định kỳ",
        "no_templates": "Chưa có mẫu giao dịch.",
        "no_recurring": "Chưa phát hiện giao dịch định kỳ.",
        "recurring_badge": "Định kỳ",

        "chart_income": "Thu",
        "chart_expense": "Chi",
        "chart_net": "Ròng",
        "chart_budget": "Ngân sách",
        "chart_spent": "Đã chi",

        "within_budget": "Trong ngân sách",
        "near_budget_limit": "Sắp chạm ngưỡng",
        "over_budget": "Vượt ngân sách",
        "remaining": "Còn lại",
        "usage": "Tỷ lệ dùng",

        "table_date": "Ngày",
        "table_type": "Loại",
        "table_category": "Danh mục",
        "table_account": "Tài khoản",
        "table_amount": "Số tiền",
        "table_note": "Ghi chú",

        "type_income": "thu",
        "type_expense": "chi",
        "type_transfer": "chuyển",
        "nav_goals": "Mục tiêu",
        "nav_recurring": "Định kỳ",

        "goals_title": "Mục tiêu tài chính",
        "goals_subtitle": "Theo dõi mục tiêu tiết kiệm và tiến độ hoàn thành.",
        "recurring_title": "Giao dịch định kỳ",
        "recurring_subtitle": "Quản lý các khoản thu, chi và chuyển tiền lặp lại.",
        "transactions_title": "Lịch sử giao dịch",
        "transactions_subtitle": "Theo dõi thu nhập, chi tiêu và chuyển tiền tại một nơi.",
        "categories_title": "Quản lý danh mục",
        "categories_subtitle": "Tạo và sắp xếp danh mục thu nhập và chi tiêu.",
        "budgets_title": "Quản lý ngân sách",
        "budgets_subtitle": "Thiết lập và theo dõi ngân sách theo từng danh mục.",
        "accounts_title": "Quản lý ví tiền",
        "accounts_subtitle": "Quản lý tiền mặt, tài khoản ngân hàng và ví điện tử.",

        "add_goal": "Thêm mục tiêu",
        "add_recurring": "Thêm định kỳ",
        "apply_now": "Áp dụng ngay",
        "open": "Mở",
        "current": "Hiện tại",
        "target": "Mục tiêu",
        "remaining_plain": "Còn lại",
        "deadline": "Hạn chót",
        "completed": "Hoàn thành",
        "due": "Đến hạn",
        "source": "Nguồn",
        "destination": "Đích",
        "next_due": "Ngày tới hạn",
        "frequency": "Tần suất",
        "weekly": "Hàng tuần",
        "monthly": "Hàng tháng",
        "amount": "Số tiền",
        "title": "Tiêu đề",
        "notes": "Ghi chú",
        "cancel": "Hủy",
        "save_goal": "Lưu mục tiêu",
        "save_recurring": "Lưu định kỳ",
        "create_first_goal": "Tạo mục tiêu đầu tiên",
        "create_first_recurring": "Tạo giao dịch định kỳ đầu tiên",
        "no_goals_yet": "Chưa có mục tiêu tài chính nào.",
        "no_recurring_yet": "Chưa có giao dịch định kỳ nào.",
        "no_recurring_due": "Không có giao dịch định kỳ nào đến hạn trong 7 ngày tới.",
        "goals_overview": "Tổng quan mục tiêu",
        "recurring_due_soon": "Sắp đến hạn",
    },
    "en": {
        "app_name": "Expense Manager",
        "nav_dashboard": "Dashboard",
        "nav_transactions": "Transactions",
        "nav_wallets": "Wallets",
        "nav_categories": "Categories",
        "nav_budgets": "Budgets",
        "logout": "Logout",
        "quick_actions": "Quick Actions",
        "view_all_transactions": "View All Transactions",
        "manage_budgets": "Manage Budgets",

        "dashboard_title": "Dashboard",
        "dashboard_overview": "Overview for {month}/{year}",
        "total_income": "Total Income",
        "total_expense": "Total Expense",
        "net_cashflow": "Net Cashflow",
        "wallet_balance": "Wallet Balance",
        "transactions_this_month": "Transactions This Month",
        "largest_expense": "Largest Expense",
        "expense_categories_used": "Expense Categories Used",
        "budget_risk": "Budget Risk",
        "cashflow_trend": "Cashflow Trend",
        "expense_breakdown": "Expense Breakdown",
        "budget_vs_spent": "Budget vs Spent",
        "wallet_distribution": "Wallet Distribution",
        "budget_alerts": "Budget Alerts",
        "top_spending_categories": "Top Spending Categories",
        "recent_transactions": "Recent Transactions",
        "see_all": "See all",

        "quick_add_title": "Quick Add",
        "quick_add_hint": "Save a transaction in one line.",
        "quick_add_examples": "Examples: 45k coffee, 120k lunch, 100k clothes, 500k transfer to Momo",
        "quick_add_placeholder": "Type something like: 45k coffee or 500k transfer Momo",
        "save_fast": "Save Fast",
        "one_tap_repeat": "One-tap Repeat",
        "recurring_suggestions": "Recurring Suggestions",
        "no_templates": "No transaction templates yet.",
        "no_recurring": "No recurring pattern detected yet.",
        "recurring_badge": "Recurring",

        "chart_income": "Income",
        "chart_expense": "Expense",
        "chart_net": "Net",
        "chart_budget": "Budget",
        "chart_spent": "Spent",

        "within_budget": "Within budget",
        "near_budget_limit": "Near budget limit",
        "over_budget": "Over budget",
        "remaining": "Remaining",
        "usage": "Usage",

        "table_date": "Date",
        "table_type": "Type",
        "table_category": "Category",
        "table_account": "Account",
        "table_amount": "Amount",
        "table_note": "Note",

        "type_income": "income",
        "type_expense": "expense",
        "type_transfer": "transfer",
        "nav_goals": "Goals",
        "nav_recurring": "Recurring",

        "goals_title": "Financial Goals",
        "goals_subtitle": "Track your savings targets and progress.",
        "recurring_title": "Recurring Transactions",
        "recurring_subtitle": "Manage repeating income, expenses, and transfers.",
        "transactions_title": "Transaction History",
        "transactions_subtitle": "Track income, expenses, and transfers in one place.",
        "categories_title": "Category Management",
        "categories_subtitle": "Create and organize your income and expense categories.",
        "budgets_title": "Budget Management",
        "budgets_subtitle": "Set and monitor budgets by category.",
        "accounts_title": "Wallet Management",
        "accounts_subtitle": "Manage your cash, bank accounts, and e-wallets.",

        "add_goal": "Add Goal",
        "add_recurring": "Add Recurring",
        "apply_now": "Apply Now",
        "open": "Open",
        "current": "Current",
        "target": "Target",
        "remaining_plain": "Remaining",
        "deadline": "Deadline",
        "completed": "Completed",
        "due": "Due",
        "source": "Source",
        "destination": "Destination",
        "next_due": "Next Due",
        "frequency": "Frequency",
        "weekly": "Weekly",
        "monthly": "Monthly",
        "amount": "Amount",
        "title": "Title",
        "notes": "Notes",
        "cancel": "Cancel",
        "save_goal": "Save Goal",
        "save_recurring": "Save Recurring",
        "create_first_goal": "Create First Goal",
        "create_first_recurring": "Create First Recurring Transaction",
        "no_goals_yet": "No financial goals yet.",
        "no_recurring_yet": "No recurring transactions yet.",
        "no_recurring_due": "No recurring transactions due in the next 7 days.",
        "goals_overview": "Goals Overview",
        "recurring_due_soon": "Recurring Due Soon",
    },
}


SERVER_MESSAGES = {
    "invalid_login": {
        "vi": "Sai tên đăng nhập hoặc mật khẩu.",
        "en": "Invalid username or password.",
    },
    "register_required": {
        "vi": "Tên đăng nhập và mật khẩu là bắt buộc.",
        "en": "Username and password are required.",
    },
    "password_mismatch": {
        "vi": "Mật khẩu xác nhận không khớp.",
        "en": "Passwords do not match.",
    },
    "username_exists": {
        "vi": "Tên đăng nhập đã tồn tại.",
        "en": "Username already exists.",
    },
    "email_exists": {
        "vi": "Email đã tồn tại.",
        "en": "Email already exists.",
    },
    "register_success": {
        "vi": "Tạo tài khoản thành công.",
        "en": "Account created successfully.",
    },
    "quick_add_empty": {
        "vi": "Hãy nhập nội dung để Thêm nhanh.",
        "en": "Please enter something for Quick Add.",
    },
    "quick_add_need_amount": {
        "vi": "Thêm nhanh cần có số tiền, ví dụ: 45k cafe hoặc 3tr lương.",
        "en": "Quick Add needs an amount, for example: 45k coffee or 3tr salary.",
    },
    "quick_add_no_target_account": {
        "vi": "Không tìm thấy tài khoản đích cho giao dịch chuyển tiền. Ví dụ đúng: 500k chuyển Momo.",
        "en": "Could not detect the destination account for transfer. Example: 500k transfer Momo.",
    },
    "quick_add_no_source_account": {
        "vi": "Không có tài khoản nguồn phù hợp để chuyển tiền.",
        "en": "No suitable source account available for transfer.",
    },
    "quick_add_not_enough_source_balance": {
        "vi": "Số dư tài khoản nguồn không đủ.",
        "en": "Not enough balance in the source account.",
    },
    "quick_add_no_account": {
        "vi": "Không tìm thấy tài khoản phù hợp.",
        "en": "No suitable account found.",
    },
    "quick_add_no_expense_category": {
        "vi": "Không tìm thấy category phù hợp cho “{text}”. Hãy tạo category mới trong Categories hoặc nhập rõ hơn. Category hiện có: {categories}.",
        "en": "Could not find a suitable category for “{text}”. Create a new category in Categories or type more clearly. Current categories: {categories}.",
    },
    "quick_add_no_income_category": {
        "vi": "Không tìm thấy category thu nhập phù hợp cho “{text}”. Hãy tạo category mới trong Categories hoặc nhập rõ hơn. Category hiện có: {categories}.",
        "en": "Could not find a suitable income category for “{text}”. Create a new category in Categories or type more clearly. Current categories: {categories}.",
    },
    "quick_add_need_create_expense_category": {
        "vi": "Chưa có category chi tiêu nào. Hãy vào Categories để tạo trước.",
        "en": "There are no expense categories yet. Please create one in Categories first.",
    },
    "quick_add_need_create_income_category": {
        "vi": "Chưa có category thu nhập nào. Hãy vào Categories để tạo trước.",
        "en": "There are no income categories yet. Please create one in Categories first.",
    },
    "quick_add_not_enough_balance": {
        "vi": "Số dư tài khoản không đủ.",
        "en": "Not enough balance in the selected account.",
    },
    "quick_add_saved": {
        "vi": "Đã lưu: {type_label} • {amount} • {account}",
        "en": "Saved: {type_label} • {amount} • {account}",
    },
    "repeat_success": {
        "vi": "Đã lặp lại giao dịch thành công.",
        "en": "Transaction repeated successfully.",
    },
    "repeat_not_found": {
        "vi": "Không tìm thấy giao dịch mẫu để lặp lại.",
        "en": "Template transaction not found.",
    },
    "repeat_failed": {
        "vi": "Không thể lặp lại giao dịch.",
        "en": "Could not repeat transaction.",
    },
    "create_success_account": {
        "vi": "Tạo tài khoản thành công.",
        "en": "Account created successfully.",
    },
    "delete_success_account": {
        "vi": "Xóa tài khoản thành công.",
        "en": "Account deleted successfully.",
    },
    "create_success_category": {
        "vi": "Tạo category thành công.",
        "en": "Category created successfully.",
    },
    "delete_success_category": {
        "vi": "Xóa category thành công.",
        "en": "Category deleted successfully.",
    },
    "create_success_budget": {
        "vi": "Tạo ngân sách thành công.",
        "en": "Budget created successfully.",
    },
    "delete_success_budget": {
        "vi": "Xóa ngân sách thành công.",
        "en": "Budget deleted successfully.",
    },
    "create_success_transaction": {
        "vi": "Tạo giao dịch thành công.",
        "en": "Transaction created successfully.",
    },
    "delete_success_transaction": {
        "vi": "Xóa giao dịch thành công.",
        "en": "Transaction deleted successfully.",
    },
    "invalid_transaction_type": {
        "vi": "Loại giao dịch không hợp lệ.",
        "en": "Invalid transaction type.",
    },
    "amount_invalid": {
        "vi": "Số tiền phải lớn hơn 0.",
        "en": "Amount must be greater than 0.",
    },
    
}


def get_lang_from_request(request):
    lang = request.session.get("lang", "vi")
    return lang if lang in SUPPORTED_LANGS else "vi"


def get_ui_texts(lang):
    return UI_TEXTS.get(lang, UI_TEXTS["vi"])


def tr(request, key, **kwargs):
    lang = get_lang_from_request(request)
    text = SERVER_MESSAGES.get(key, {}).get(lang) or SERVER_MESSAGES.get(key, {}).get("en") or key
    try:
        return text.format(**kwargs)
    except Exception:
        return text