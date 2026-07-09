package com.revature.expensemanager;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DatabaseConnection {

    // Path to the SQLite database created by the Python app
    private static final Logger logger =
        LoggerFactory.getLogger(DatabaseConnection.class);
    private static final String URL = "jdbc:sqlite:../employee_app/expense_manager.db";

    public static Connection getConnection() throws SQLException {
        logger.debug("Opening SQLite database connection.");
        return DriverManager.getConnection(URL);
    }
}