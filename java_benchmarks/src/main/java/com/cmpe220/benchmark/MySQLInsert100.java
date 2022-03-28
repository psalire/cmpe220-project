package com.cmpe220.benchmark;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
* REQUIRED: have MySQL already running
*/
public class MySQLInsert100 extends AbstractBenchmark {

    private Connection conn;
    private Statement stmt;

    public MySQLInsert100() {
        category = "mysql";
        description = "This is an example";
    }

    public void setupQuery() {
        System.out.println("Connecting to MySQL...");
        try {
            conn = DriverManager.getConnection(
                "jdbc:mysql://localhost/",
                "root",
                "root-password123"
            );
            stmt = conn.createStatement();

            stmt.executeUpdate("CREATE DATABASE cmpe220db");
            conn.close();
            // stmt.executeUpdate("USE cmpe220db");
            conn = DriverManager.getConnection(
                "jdbc:mysql://localhost/cmpe220db",
                "root",
                "root-password123"
            );
            stmt = conn.createStatement();

            stmt.executeUpdate(
                "CREATE TABLE fivecolumns(col1 VARCHAR(14) PRIMARY KEY,col2 TEXT,col3 TEXT,col4 TEXT,col5 TEXT)"
            );
        }
        catch (SQLException e) {
            System.out.println(e.toString());
        }
    }

    public void endQuery() {
        System.out.println("Closing...");
        try {
            stmt.executeUpdate("DROP DATABASE cmpe220db");
            conn.close();
        }
        catch (SQLException e) {
            System.out.println(e.toString());
        }
    }

    public void runQuery() {
        try {
            for (int i=0; i<100; i++) {
                stmt.executeUpdate(
                    "INSERT INTO fivecolumns(col1, col2, col3, col4, col5) "+
                    "VALUES ('Rutuja_"+i+"', 'Palatkar', 'SJSU', 'Student', 'ID')"
                );
            }
        }
        catch (SQLException e) {
            System.out.println(e);
        }
    }
}
