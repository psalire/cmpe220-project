package com.cmpe220.benchmark;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

import com.mongodb.*;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import org.bson.Document;
import org.bson.types.Binary;

import com.mongodb.client.MongoClient;

/**
* REQUIRED: have Cassandra DB already running
*/
public class MongoInsert100UnstructuredInsertOne extends AbstractBenchmark {

    private MongoClient client;
    private MongoDatabase db;
    private MongoCollection<Document> col;
    private ArrayList<Document> data;

    public MongoInsert100UnstructuredInsertOne () {
        category = "mongo";
        description = "This is an example";
    }

    public void setupQuery() throws Exception {
        System.out.println("Connecting to mongo...");
        client = MongoClients.create("mongodb://localhost:27017/");
        db = client.getDatabase("mydb");
        String colName = "mycol";
        db.createCollection(colName);
        col = db.getCollection(colName);
        data = new ArrayList<Document>();
        for (int i=0; i<100; i++) {
            data.add(new Document(
                String.format("cat_%d", i),
                new Binary(
                    Files.readAllBytes(Paths.get("data/cat.JPG"))
                )
            ));
        }
    }

    public void endQuery() {
        System.out.println("Closing...");
        col.drop();
        client.close();
    }

    public void runQuery() {
        for (int i=0; i<data.size(); i++) {
            col.insertOne(data.get(i));
        }
    }
}
