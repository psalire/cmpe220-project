'''
REQUIRED: have Cassandra DB already running
pip install cassandra-driver (https://docs.datastax.com/en/developer/python-driver/3.25/)

(This is run from the parent directory, so
"python_benchmarks.AbstractBenchmark"
is required instead of "AbstractBenchmark")
'''
from python_benchmarks.AbstractBenchmark import AbstractBenchmark
import pymongo


class Mongo_Select100(AbstractBenchmark):

    def __init__(self):
        self.category = 'mongo'
        self.description = 'This is an example'

    def setupQuery(self):
        print('Connecting to mongo...')
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['mydb']
        self.col = self.db['mycol']
        self.col.insert_many([{
            'fname': 'Rutuja',
            'lname': 'Palatkar',
            'school': 'SJSU',
            'role': 'Student',
            'id': 'ID',
        } for _ in range(100)])

    def endQuery(self):
        self.col.drop()
        self.client.close()

    def runQuery(self):
        x = [y for y in self.col.find()]
