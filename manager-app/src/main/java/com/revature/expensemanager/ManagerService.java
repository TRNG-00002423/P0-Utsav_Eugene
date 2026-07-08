package com.revature.expensemanager;

public class ManagerService {
    private final ManagerDao dao = new ManagerDaoImpl();

    public int login(String username, String password){
        return dao.login(username, password);
    }
    public void viewPendingExpenses() {
        dao.viewPendingExpenses();
    }

    public void updateExpenseStatus(int expenseId,int managerId,String status,String comment){
        dao.updateExpenseStatus(expenseId, managerId, status, comment);
    } 
    
    public void reportByEmployee() {
        dao.reportByEmployee();
    }

    public void reportByCategory() {
        dao.reportByCategory();
    }

    public void reportByDate() {
        dao.reportByDate();
    }
}
