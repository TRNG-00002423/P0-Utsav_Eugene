from database import setup_database
from expense_service import login, submit_expense, view_my_expenses


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
        print("3. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            submit_expense(user_id)

        elif choice == "2":
            view_my_expenses(user_id)

        elif choice == "3":
            print("Logged out.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()