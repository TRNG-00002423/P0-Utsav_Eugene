from datetime import date
from database import get_connection


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid number.")


def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, role
        FROM users
        WHERE username = ? AND password = ? AND role = 'employee'
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    return user


def submit_expense(user_id):
    amount = get_valid_amount()
    category = input("Enter category: ")
    description = input("Enter description: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (user_id, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, amount, category, description, str(date.today())))

    expense_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO approvals (expense_id, status)
        VALUES (?, 'pending')
    """, (expense_id,))

    conn.commit()
    conn.close()

    print("Expense submitted successfully.")


def view_my_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, e.amount, e.category, e.description, e.date, a.status, a.comment
        FROM expenses e
        JOIN approvals a ON e.id = a.expense_id
        WHERE e.user_id = ?
    """, (user_id,))

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("No expenses found.")
        return

    for expense in expenses:
        print("\n----------------------")
        print(f"Expense ID: {expense[0]}")
        print(f"Amount: ${expense[1]:.2f}")
        print(f"Category: {expense[2]}")
        print(f"Description: {expense[3]}")
        print(f"Date: {expense[4]}")
        print(f"Status: {expense[5]}")
        print(f"Comment: {expense[6] if expense[6] else 'No comment'}")


def edit_pending_expense(user_id):
    expense_id = input("Enter expense ID to edit: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, e.amount, e.category, e.description, a.status
        FROM expenses e
        JOIN approvals a ON e.id = a.expense_id
        WHERE e.id = ? AND e.user_id = ? AND a.status = 'pending'
    """, (expense_id, user_id))

    expense = cursor.fetchone()

    if expense is None:
        print("Expense not found, or it is not pending.")
        conn.close()
        return

    print("\nCurrent Expense:")
    print(f"Amount: ${expense[1]:.2f}")
    print(f"Category: {expense[2]}")
    print(f"Description: {expense[3]}")
    print(f"Status: {expense[4]}")

    new_amount = get_valid_amount()
    new_category = input("Enter new category: ")
    new_description = input("Enter new description: ")

    cursor.execute("""
        UPDATE expenses
        SET amount = ?, category = ?, description = ?
        WHERE id = ? AND user_id = ?
    """, (new_amount, new_category, new_description, expense_id, user_id))

    conn.commit()
    conn.close()

    print("Expense updated successfully.")


def delete_pending_expense(user_id):
    expense_id = input("Enter expense ID to delete: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, a.status
        FROM expenses e
        JOIN approvals a ON e.id = a.expense_id
        WHERE e.id = ? AND e.user_id = ? AND a.status = 'pending'
    """, (expense_id, user_id))

    expense = cursor.fetchone()

    if expense is None:
        print("Expense not found, or it is not pending.")
        conn.close()
        return

    cursor.execute("""
        DELETE FROM approvals
        WHERE expense_id = ?
    """, (expense_id,))

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ? AND user_id = ?
    """, (expense_id, user_id))

    conn.commit()
    conn.close()

    print("Expense deleted successfully.")


def view_expense_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, e.amount, e.category, e.description, e.date, a.status, a.comment, a.review_date
        FROM expenses e
        JOIN approvals a ON e.id = a.expense_id
        WHERE e.user_id = ?
        AND a.status IN ('approved', 'denied')
    """, (user_id,))

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("No approved or denied expenses found.")
        return

    print("\n=== Expense History ===")

    for expense in expenses:
        print("\n----------------------")
        print(f"Expense ID: {expense[0]}")
        print(f"Amount: ${expense[1]:.2f}")
        print(f"Category: {expense[2]}")
        print(f"Description: {expense[3]}")
        print(f"Date Submitted: {expense[4]}")
        print(f"Status: {expense[5]}")
        print(f"Comment: {expense[6] if expense[6] else 'No comment'}")
        print(f"Review Date: {expense[7] if expense[7] else 'Not reviewed'}")