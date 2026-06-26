package com.revature.expensemanager;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ManagerService {
    public static void reportByEmployee() {
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
public static void reportByCategory() {
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

public static void reportByDate() {
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