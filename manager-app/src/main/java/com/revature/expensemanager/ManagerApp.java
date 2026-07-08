package com.revature.expensemanager;

import java.util.Scanner;

public class ManagerApp {

    private static int getValidExpenseId(Scanner scanner) {
        while (true) {
            System.out.print("Enter expense ID: ");

            try {
                int expenseId = Integer.parseInt(scanner.nextLine());

                if (expenseId <= 0) {
                    System.out.println("Expense ID must be greater than 0.");
                    continue;
                }

                return expenseId;

            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
            }
        }
    }

    public static void main(String[] args) {
        ManagerService managerService = new ManagerService();
        Scanner scanner = new Scanner(System.in);

        System.out.println("================================");
        System.out.println(" Revature Expense Manager");
        System.out.println(" Manager Application");
        System.out.println("================================");

        System.out.print("Username: ");
        String username = scanner.nextLine();

        System.out.print("Password: ");
        String password = scanner.nextLine();

        int managerId = managerService.login(username, password);

        if (managerId == -1) {
            System.out.println("Invalid manager login.");
            scanner.close();
            return;
        }

        System.out.println("Welcome, " + username + "!");

        while (true) {
            System.out.println("\n==============================");
            System.out.println(" Manager Expense Menu");
            System.out.println("==============================");
            System.out.println("1. View Pending Expenses");
            System.out.println("2. Approve Expense");
            System.out.println("3. Deny Expense");
            System.out.println("4. Report By Employee");
            System.out.println("5. Report By Category");
            System.out.println("6. Report By Date");
            System.out.println("7. Logout");

            System.out.print("\nChoose an option: ");
            String choice = scanner.nextLine();

            if (choice.equals("1")) {

                managerService.viewPendingExpenses();

            } else if (choice.equals("2")) {

                int expenseId = getValidExpenseId(scanner);

                System.out.print("Enter comment: ");
                String comment = scanner.nextLine();

                managerService.updateExpenseStatus(expenseId, managerId, "approved", comment);

            } else if (choice.equals("3")) {

                int expenseId = getValidExpenseId(scanner);

                System.out.print("Enter comment: ");
                String comment = scanner.nextLine();

                managerService.updateExpenseStatus(expenseId, managerId, "denied", comment);

            } else if (choice.equals("4")) {

                managerService.reportByEmployee();

            } else if (choice.equals("5")) {

                managerService.reportByCategory();

            } else if (choice.equals("6")) {

                managerService.reportByDate();

            } else if (choice.equals("7")) {

                System.out.println("Logged out.");
                break;

            } else {

                System.out.println("Invalid choice. Please choose 1-7.");
            }
        }

        scanner.close();
    }
}