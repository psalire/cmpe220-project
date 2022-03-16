package com.cmpe220.benchmark;

import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.*;

/**
* REQUIRED: have Cassandra DB already running
*/
public class CassandraInsert100 extends AbstractBenchmark {

    private CqlSession session;

    public CassandraInsert100() {
        category = "Read";
        description = "This is an example";
    }

    public void setupQuery() {
        System.out.println("Connecting to cassandra...");
        session = CqlSession.builder().build();

        try {
            session.execute("DROP KEYSPACE cmpe220KS");
        }
        catch (Exception e) {}
        session.execute(
            "CREATE KEYSPACE cmpe220KS "+
            "WITH replication="+
            "{'class':'SimpleStrategy','replication_factor':1}"
        );
        session.execute("USE cmpe220KS");
        session.execute(
            "CREATE TABLE fivecolumns(col1 TEXT PRIMARY KEY,col2 TEXT,col3 TEXT,col4 TEXT,col5 TEXT)"
        );
    }

    public void endQuery() {
        System.out.println("Closing...");
        session.execute("DROP KEYSPACE cmpe220KS");
        session.close();
    }

    public void runQuery() {
        for (int i=0; i<100; i++) {
            session.execute(
                "INSERT INTO fivecolumns(col1, col2, col3, col4, col5) VALUES ('Rutuja', 'Palatkar', 'SJSU', 'Student', 'ID')");
        }
    }
}
