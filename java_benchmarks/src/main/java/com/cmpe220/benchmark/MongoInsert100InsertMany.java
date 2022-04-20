package com.cmpe220.benchmark;

import java.util.ArrayList;

import com.mongodb.*;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import org.bson.Document;

import com.mongodb.client.MongoClient;

/**
* REQUIRED: have Cassandra DB already running
*/
public class MongoInsert100InsertMany extends AbstractBenchmark {

    private MongoClient client;
    private MongoDatabase db;
    private MongoCollection<Document> col;
    private ArrayList<Document> data;

    public MongoInsert100InsertMany() {
        category = "mongo";
        description = "This is an example";
    }

    public void setupQuery() {
        System.out.println("Connecting to mongo...");
        client = MongoClients.create("mongodb://localhost:27017/");
        db = client.getDatabase("mydb");
        String colName = "mycol";
        db.createCollection(colName);
        col = db.getCollection(colName);
        data = new ArrayList<Document>();
        for (int i=0; i<100; i++) {
            data.add(
                new Document("fname", "Rutuja")
                    .append("lname", "Palatkar")
                    .append("school", "SJSU")
                    .append("role", "Student")
                    .append("id", "ID")
            );
        }
    }

    public void endQuery() {
        System.out.println("Closing...");
        col.drop();
        client.close();
    }

    public void runQuery() {
        col.insertMany(data);
    }
}
