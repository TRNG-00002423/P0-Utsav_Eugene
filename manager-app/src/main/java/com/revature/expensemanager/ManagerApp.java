package com.revature.expensemanager;

import java.util.Scanner;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ManagerApp {
    private static final Logger logger =
        LoggerFactory.getLogger(ManagerApp.class);
    private static int getValidExpenseId(Scanner scanner) {
        while (true) {
            System.out.print("Enter expense ID: ");

            try {
                int expenseId = Integer.parseInt(scanner.nextLine());

                if (expenseId <= 0) {
                    logger.warn("Invalid expense ID input received, must be greater than 0.");
                    System.out.println("Please enter a valid number: ");
                    continue;
                }

                return expenseId;

            } catch (NumberFormatException e) {
                logger.warn("Invalid expense ID input received, must be greater than 0.");
                System.out.println("Please enter a valid number.");
            }
        }
    }

    public static void main(String[] args) {
        logger.info("Manager application started.");
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
        logger.info("Manager login attempted for username: {}", username);
        int managerId = managerService.login(username, password);

        if (managerId == -1) {
            logger.warn("Manager login failed for username: {}", username);
            System.out.println("Invalid manager login.");
            scanner.close();
            return;
        }
        logger.debug("Successful login for: {}", username);
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
            logger.info("Manager selected menu option: {}", choice);

            if (choice.equals("1")) {
                logger.info("Manager {} requested pending expenses.", managerId);
                managerService.viewPendingExpenses();

            } else if (choice.equals("2")) {

                int expenseId = getValidExpenseId(scanner);

                System.out.print("Enter comment: ");
                String comment = scanner.nextLine();
                logger.info("Manager {} requested to approve expense {}.", managerId, expenseId);
                managerService.updateExpenseStatus(expenseId, managerId, "approved", comment);

            } else if (choice.equals("3")) {

                int expenseId = getValidExpenseId(scanner);

                System.out.print("Enter comment: ");
                String comment = scanner.nextLine();
                logger.info("Manager {} requested to deny expense {}.", managerId, expenseId);
                managerService.updateExpenseStatus(expenseId, managerId, "denied", comment);

            } else if (choice.equals("4")) {
                logger.info("Manager {} requested report by employee.", managerId);
                managerService.reportByEmployee();

            } else if (choice.equals("5")) {
                logger.info("Manager {} requested report by category.", managerId);
                managerService.reportByCategory();

            } else if (choice.equals("6")) {
                logger.info("Manager {} requested report by date.", managerId);
                managerService.reportByDate();

            } else if (choice.equals("7")) {

                System.out.println("Logged out.");
                break;

            } else {
                logger.warn("Invalid menu choice entered: {}", choice);
                System.out.println("Invalid choice. Please choose 1-7.");
            }
        }
        logger.info("Manager {} logged out.", managerId);
        scanner.close();
    }
}