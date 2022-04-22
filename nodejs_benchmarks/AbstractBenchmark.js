
class AbstractBenchmark {

    constructor() {
        if (this.constructor == AbstractBenchmark) {
            throw new Error("AbstractBenchmark is abstract");
        }
        this.category = '';
        this.description = '';
    }

    /**
    * Operations before the actual query
    * e.g. connection, initializations, etc.
    */
    setupQuery() {

    }

    /**
    * Operations after the query
    * e.g. cleanup, shutdown, etc.
    */
    endQuery() {

    }

    /**
    * Operations before the actual query
    * e.g. connection, initializations, etc.
    */
    runQuery() {
        throw new Error("runQuery must be implemented");
    }

    /**
    * send milliseconds that the query took over TCP
    */
    benchmark() {
        this.setupQuery();

        var start_time = performance.now();
        this.runQuery();
        var end_time = performance.now();

        this.endQuery();
        // TODO: send return val over IPC with TCP
        return (end_time - start_time) / 1000000;
    }

    getCategory() {
        return this.category;
    }

    getDescription() {
        return this.description;
    }
}

module.exports = {
    AbstractBenchmark,
}
