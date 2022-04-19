package com.cmpe220.benchmark;

abstract public class AbstractBenchmark {

    protected String category;
    protected String description;

    /**
    * Operations before the actual query
    * e.g. connection, initializations, etc.
    */
    protected void setupQuery() throws Exception {

    }

    /**
    * Operations after the query
    * e.g. cleanup, shutdown, etc.
    */
    protected void endQuery() throws Exception {

    }

    /**
    * Run the query to benchmark
    * Make sure that the query is synchronous!
    */
    abstract protected void runQuery() throws Exception;

    /**
    * @return milliseconds that the query took
    */
    public long benchmark() throws Exception {
        setupQuery();

        long startTime = System.currentTimeMillis();
        runQuery();
        long endTime = System.currentTimeMillis();

        endQuery();
        return endTime - startTime;
    }

    public String getCategory() {
        return category;
    }

    public String getDescription() {
        return description;
    }
}
