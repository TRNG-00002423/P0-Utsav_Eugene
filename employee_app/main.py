from database import setup_database
from expense_service import login, submit_expense, view_my_expenses, edit_pending_expense, delete_pending_expense, view_expense_history


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
        print("\n==============================")
        print(" Employee Expense Menu")
        print("==============================")
        print("1. Submit Expense")
        print("2. View My Expenses")
        print("3. Edit Pending Expense")
        print("4. Delete Pending Expense")
        print("5. View Approved/Denied History")
        print("6. Logout")

        choice = input("\nChoose an option: ")

        if choice == "1":
            submit_expense(user_id)

        elif choice == "2":
            view_my_expenses(user_id)

        elif choice == "3":
            edit_pending_expense(user_id)

        elif choice == "4":
            delete_pending_expense(user_id)

        elif choice == "5":
            view_expense_history(user_id)

        elif choice == "6":
            print("Logged out.")
            break

        else:
            print("Invalid choice. Please choose 1-6.")


if __name__ == "__main__":
    main()