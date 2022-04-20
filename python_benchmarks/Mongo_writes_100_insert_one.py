'''
REQUIRED: have Cassandra DB already running
pip install cassandra-driver (https://docs.datastax.com/en/developer/python-driver/3.25/)

(This is run from the parent directory, so
"python_benchmarks.AbstractBenchmark"
is required instead of "AbstractBenchmark")
'''
from python_benchmarks.AbstractBenchmark import AbstractBenchmark
import pymongo


class Mongo_writes_100_insert_one(AbstractBenchmark):

    def __init__(self):
        self.category = 'mongo'
        self.description = 'This is an example'

    def setupQuery(self):
        print('Connecting to mongo...')
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['mydb']
        self.col = self.db['mycol']
        self.data = [{
            'fname': 'Rutuja',
            'lname': 'Palatkar',
            'school': 'SJSU',
            'role': 'Student',
            'id': 'ID',
        } for _ in range(100)]

    def endQuery(self):
        self.col.drop()
        self.client.close()

    def runQuery(self):
        for i in range(100):
            self.col.insert_one(self.data[i])
