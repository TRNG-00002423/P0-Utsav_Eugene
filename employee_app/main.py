from database import setup_database
from expense_service import login, submit_expense, view_approval_history, view_expense_status, view_my_expenses


def main():
    setup_database()

    print("=== Employee Expense App ===")

    username = input("Username: ")
    password = input("Password: ")

    user = login(username, password)

    if user is None:
        print("Invalid employee login.")
        return

    user_id = user[0]
    print(f"Welcome, {user[1]}!")

    while True:
        print("\n--- Menu ---")
        print("1. Submit Expense")
        print("2. View My Expenses")
        print("3. View Submitted Expense Status")
        print("4. View Approval History")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            submit_expense(user_id)

        elif choice == "2":
            view_my_expenses(user_id)
        
        elif choice == "3":
            view_expense_status(user_id)
        
        elif choice == "4":
            view_approval_history(user_id)

        elif choice == "5":
            print("Logged out.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()