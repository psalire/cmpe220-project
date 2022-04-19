package com.cmpe220.benchmark;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
* REQUIRED: have MySQL already running
*/
public class MySQLCreateTable5Columns extends AbstractBenchmark {

    private Connection conn;
    private Statement stmt;

    public MySQLCreateTable5Columns() {
        category = "mysql";
        description = "This is an example";
    }

    public void setupQuery() throws SQLException {
        System.out.println("Connecting to MySQL...");
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
    }

    public void endQuery() throws SQLException {
        System.out.println("Closing...");
        stmt.executeUpdate("DROP DATABASE cmpe220db");
        conn.close();
    }

    public void runQuery() throws SQLException {
        stmt.executeUpdate(
            "CREATE TABLE fivecolumns(col1 VARCHAR(14) PRIMARY KEY,col2 TEXT,col3 TEXT,col4 TEXT,col5 TEXT)"
        );
    }
}
