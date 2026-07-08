package com.revature.expensemanager;

public interface ManagerDao {
    int login(String username, String password);

    void viewPendingExpenses();

    void updateExpenseStatus(
            int expenseId,
            int managerId,
            String status,
            String comment
    );

    void reportByEmployee();

    void reportByCategory();

    void reportByDate();
}
