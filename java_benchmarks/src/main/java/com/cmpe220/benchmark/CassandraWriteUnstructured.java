package com.cmpe220.benchmark;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;

import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.*;

/**
* REQUIRED: have Cassandra DB already running
*/
public class CassandraWriteUnstructured extends AbstractBenchmark {

    private CqlSession session;
    private String img_blob;

    public CassandraWriteUnstructured() {
        category = "cassandra";
        description = "This is an example";
    }

    public void setupQuery() throws IOException {
        System.out.println("Connecting to cassandra...");
        session = CqlSession.builder().build();

        session.execute(
            "CREATE KEYSPACE cmpe220KS "+
            "WITH replication="+
            "{'class':'SimpleStrategy','replication_factor':1}"
        );
        session.execute("USE cmpe220KS");
        session.execute("CREATE TABLE tbl (col1 INT PRIMARY KEY, col2 MAP<TEXT, BLOB>)");
        img_blob = new String(
            Base64.getEncoder().encode(
                Files.readAllBytes(Paths.get("data/cat.JPG"))
            )
        );
    }

    public void endQuery() {
        System.out.println("Closing...");
        session.execute("DROP KEYSPACE cmpe220KS");
        session.close();
    }

    public void runQuery() {
        session.execute(
            String.format(
                "INSERT INTO tbl (col1, col2) VALUES(1, {'cat': textAsBlob('%s')})", img_blob
            )
        );
    }
}
