package com.revature.expensemanager;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ManagerDaoImpl implements ManagerDao{
    @Override
    public int login(String username, String password) {
        String sql = "SELECT id FROM users WHERE username = ? AND password = ? AND role = 'manager'";

        try (
                Connection conn = DatabaseConnection.getConnection();
                PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, username);
            stmt.setString(2, password);

            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                return rs.getInt("id");
            }

            return -1;

        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return -1;
        }
    }
    
    @Override
    public void viewPendingExpenses() {
        String sql = "SELECT e.id, u.username, e.amount, e.category, e.description, e.date, a.status " +
                     "FROM expenses e " +
                     "JOIN users u ON e.user_id = u.id " +
                     "JOIN approvals a ON e.id = a.expense_id " +
                     "WHERE a.status = 'pending'";

        try (
                Connection conn = DatabaseConnection.getConnection();
                PreparedStatement stmt = conn.prepareStatement(sql);
                ResultSet rs = stmt.executeQuery()) {

            boolean found = false;

            System.out.println("\n=== Pending Expenses ===");

            while (rs.next()) {
                found = true;

                System.out.println("\n----------------------");
                System.out.println("Expense ID: " + rs.getInt("id"));
                System.out.println("Employee: " + rs.getString("username"));
                System.out.printf("Amount: $%.2f%n", rs.getDouble("amount"));
                System.out.println("Category: " + rs.getString("category"));
                System.out.println("Description: " + rs.getString("description"));
                System.out.println("Date: " + rs.getString("date"));
                System.out.println("Status: " + rs.getString("status"));
            }

            if (!found) {
                System.out.println("No pending expenses found.");
            }

        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void updateExpenseStatus(int expenseId, int managerId, String status, String comment) {
        String sql = "UPDATE approvals " +
                     "SET status = ?, reviewer = ?, comment = ?, review_date = date('now') " +
                     "WHERE expense_id = ? AND status = 'pending'";

        try (
                Connection conn = DatabaseConnection.getConnection();
                PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, status);
            stmt.setInt(2, managerId);
            stmt.setString(3, comment);
            stmt.setInt(4, expenseId);

            int rowsUpdated = stmt.executeUpdate();

            if (rowsUpdated > 0) {
                System.out.println("Expense " + status + " successfully.");
            } else {
                System.out.println("Expense not found, or it is not pending.");
            }

        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void reportByEmployee() {
    String sql = """
        SELECT u.username,
               COUNT(e.id) AS expense_count,
               SUM(e.amount) AS total_amount
        FROM expenses e
        JOIN users u ON e.user_id = u.id
        GROUP BY u.id, u.username
        """;

    try (
        Connection conn = DatabaseConnection.getConnection();
        PreparedStatement statement = conn.prepareStatement(sql);
        ResultSet results = statement.executeQuery()
    ) {
        while (results.next()) {
            System.out.println("----------------------");
            System.out.println(
                "Employee: " + results.getString("username")
            );
            System.out.println(
                "Expense Count: " + results.getInt("expense_count")
            );
            System.out.println(
                "Total Amount: $" + results.getDouble("total_amount")
            );
        }

    } catch (SQLException e) {
        System.out.println("Unable to generate employee report.");
        e.printStackTrace();
    }
}

@Override
public void reportByCategory() {
    String sql = """
        SELECT category,
               COUNT(id) AS expense_count,
               SUM(amount) AS total_amount
        FROM expenses
        GROUP BY category
        """;

    try (
        Connection conn = DatabaseConnection.getConnection();
        PreparedStatement statement = conn.prepareStatement(sql);
        ResultSet results = statement.executeQuery()
    ) {
        while (results.next()) {
            System.out.println("----------------------");
            System.out.println(
                "Category: " + results.getString("category")
            );
            System.out.println(
                "Expense Count: " + results.getInt("expense_count")
            );
            System.out.println(
                "Total Amount: $" + results.getDouble("total_amount")
            );
        }

    } catch (SQLException e) {
        System.out.println("Unable to generate category report.");
        e.printStackTrace();
    }
}

@Override
public void reportByDate() {
    String sql = """
        SELECT date,
               COUNT(id) AS expense_count,
               SUM(amount) AS total_amount
        FROM expenses
        GROUP BY date
        ORDER BY date DESC
        """;

    try (
        Connection conn = DatabaseConnection.getConnection();
        PreparedStatement statement = conn.prepareStatement(sql);
        ResultSet results = statement.executeQuery()
    ) {
        while (results.next()) {
            System.out.println("----------------------");
            System.out.println(
                "Date: " + results.getString("date")
            );
            System.out.println(
                "Expense Count: " + results.getInt("expense_count")
            );
            System.out.println(
                "Total Amount: $" + results.getDouble("total_amount")
            );
        }

    } catch (SQLException e) {
        System.out.println("Unable to generate date report.");
        e.printStackTrace();
    }
}
}