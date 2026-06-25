package com.revature.expensemanager;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {

    // Path to the SQLite database created by the Python app
    private static final String URL = "jdbc:sqlite:../employee_app/expense_manager.db";

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL);
    }
}