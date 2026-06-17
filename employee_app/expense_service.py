from datetime import date
from database import get_connection


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
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (user_id, amount, description, date)
        VALUES (?, ?, ?, ?)
    """, (user_id, amount, description, str(date.today())))

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
        SELECT e.id, e.amount, e.description, e.date, a.status, a.comment
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
        print("----------------------")
        print("Expense ID:", expense[0])
        print("Amount:", expense[1])
        print("Description:", expense[2])
        print("Date:", expense[3])
        print("Status:", expense[4])
        print("Comment:", expense[5])



def edit_expense():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
                   
        SELECT e.id, e.amount, e.description, e.date, a.status, a.comment
                   

                   
                   """)