package com.revature.expensemanager;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ManagerService {
    private static final Logger logger =
        LoggerFactory.getLogger(ManagerService.class);
    private final ManagerDao dao = new ManagerDaoImpl();

    public int login(String username, String password){
        logger.info("Processing login request for username: {}", username);
        int managerId = dao.login(username, password);

        if (managerId == -1) {
            logger.warn("Login service failed for username: {}", username);
        } else {
            logger.info("Login service succeeded for username: {}", username);
        }
        return managerId;
    }
    public void viewPendingExpenses() {
        logger.info("Processing request to view pending expenses.");
        dao.viewPendingExpenses();
    }

    public void updateExpenseStatus(int expenseId,int managerId,String status,String comment){
        logger.info("Processing request to update expense {} to status '{}'.", expenseId, status);
        dao.updateExpenseStatus(expenseId, managerId, status, comment);
    } 
    
    public void reportByEmployee() {
        logger.info("Processing report by employee request.");
        dao.reportByEmployee();
    }

    public void reportByCategory() {
        logger.info("Processing report by category request.");
        dao.reportByCategory();
    }

    public void reportByDate() {
        logger.info("Processing report by date request.");
        dao.reportByDate();
    }
}
