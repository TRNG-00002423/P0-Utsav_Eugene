from datetime import date
from database import get_connection
import bcrypt


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


def check_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, password, role
        FROM users
        WHERE username = ? AND role = 'employee'
    """, (username,))

    user = cursor.fetchone()
    conn.close()

    stored_hash = user[2]

    if check_password(password, stored_hash):
        return user
    else: 
        return None


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


def view_my_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, e.amount, e.category, e.description, e.date, a.status
        FROM expenses e
        JOIN approvals a ON e.id = a.expense_id
        WHERE e.user_id = ?
        ORDER BY e.id DESC
    """, (user_id,))

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("No expenses found.")
        return

    print("\n=== My Expenses ===")

    for expense in expenses:
        print("\n----------------------")
        print(f"Expense ID: {expense[0]}")
        print(f"Amount: ${expense[1]:.2f}")
        print(f"Category: {expense[2]}")
        print(f"Description: {expense[3]}")
        print(f"Date Submitted: {expense[4]}")
        print(f"Status: {expense[5]}")


def view_expense_status(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, e.amount, e.category, a.status
        FROM expenses e
        JOIN approvals a ON e.id = a.expense_id
        WHERE e.user_id = ?
        ORDER BY e.id DESC
    """, (user_id,))

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("No expenses found.")
        return

    print("\n=== Expense Status ===")

    for expense in expenses:
        print("----------------------")
        print("Expense ID:", expense[0])
        print(f"Amount: ${expense[1]:.2f}")
        print("Category:", expense[2])
        print("Status:", expense[3])


def view_approval_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, a.expense_id, a.status, a.comment, a.review_date
        FROM expenses e
        JOIN approvals a ON e.id = a.expense_id
        WHERE e.user_id = ?
        AND a.status IN ('approved', 'denied')
        ORDER BY a.id DESC
    """, (user_id,))

    approvals = cursor.fetchall()
    conn.close()

    if not approvals:
        print("No approved or denied expenses found.")
        return

    print("\n=== Approval History ===")

    for approval in approvals:
        print("----------------------")
        print("Approval ID:", approval[0])
        print("Expense ID:", approval[1])
        print("Status:", approval[2])
        print("Comment:", approval[3] if approval[3] else "No comment")
        print("Review Date:", approval[4] if approval[4] else "Not reviewed")


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
        ORDER BY e.id DESC
    """, (user_id,))

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("No approved or denied expenses found.")
        return

    print("\n=== Full Expense History ===")

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