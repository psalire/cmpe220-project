'''
REQUIRED: have Cassandra DB already running
pip install cassandra-driver (https://docs.datastax.com/en/developer/python-driver/3.25/)

(This is run from the parent directory, so
"python_benchmarks.AbstractBenchmark"
is required instead of "AbstractBenchmark")
'''
from python_benchmarks.AbstractBenchmark import AbstractBenchmark
from bson.binary import Binary
import pymongo


class MongoInsert100UnstructuredInsertOne(AbstractBenchmark):

    def __init__(self):
        self.category = 'mongo'
        self.description = 'This is an example'

    def setupQuery(self):
        print('Connecting to mongo...')
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['mydb']
        self.col = self.db['mycol']
        with open('data/cat.JPG', 'rb') as img:
            self.img_data = Binary(img.read())
        self.data = [{
            f'cat_{i}': self.img_data
        } for i in range(100)]

    def endQuery(self):
        self.col.drop()
        self.client.close()

    def runQuery(self):
        for i in range(100):
            self.col.insert_one(self.data[i])
