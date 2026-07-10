from database import setup_database
from expense_service import (
    login,
    submit_expense,
    view_my_expense,
    view_expense_status,
    edit_pending_expense,
    delete_pending_expense,
    view_expense_history,
    view_approval_history
)


def print_header(title):
    print("\n" + "=" * 45)
    print(title.center(45))
    print("=" * 45)


def print_menu():
    print_header("Employee Expense Menu")
    print("1. Submit Expense")
    print("2. View My Expenses")
    print("3. Edit Pending Expense")
    print("4. Delete Pending Expense")
    print("5. View Submitted Expense Status")
    print("6. View Full Expense History")
    print("7. View Approved/Denied History")
    print("8. Logout")


def pause():
    input("\nPress Enter to continue...")


def main():
    setup_database()

    print_header("Employee Expense App")

    username = input("Username: ")
    password = input("Password: ")

    user = login(username, password)

    if user is None:
        print("\nInvalid employee login.")
        return

    user_id = user[0]
    print(f"\nWelcome, {user[1]}!")

    while True:
        print_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            print_header("Submit Expense")
            submit_expense(user_id)
            pause()

        elif choice == "2":
            print_header("My Expenses")
            view_my_expense(user_id)
            pause()

        elif choice == "3":
            print_header("Edit Pending Expense")
            edit_pending_expense(user_id)
            pause()

        elif choice == "4":
            print_header("Delete Pending Expense")
            delete_pending_expense(user_id)
            pause()

        elif choice == "5":
            print_header("Expense Status")
            view_expense_status(user_id)
            pause()

        elif choice == "6":
            print_header("Full Expense History")
            view_expense_history(user_id)
            pause()

        elif choice == "7":
            print_header("Approved/Denied History")
            view_approval_history(user_id)
            pause()

        elif choice == "8":
            print("\nLogged out. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please choose 1-8.")
            pause()


if __name__ == "__main__":
    main()