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


class Mongo_Write_Unstructured(AbstractBenchmark):

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

    def endQuery(self):
        self.col.drop()

    def runQuery(self):
        self.col.insert_one({'cat': self.img_data})
