'''
REQUIRED: have Cassandra DB already running
pip install cassandra-driver (https://docs.datastax.com/en/developer/python-driver/3.25/)

(This is run from the parent directory, so
"python_benchmarks.AbstractBenchmark"
is required instead of "AbstractBenchmark")
'''
from python_benchmarks.AbstractBenchmark import AbstractBenchmark
from cassandra.cluster import Cluster
import base64

class Cassandra_Write_Unstructured_100(AbstractBenchmark):

    def __init__(self):
        self.category = 'cassandra'
        self.description = 'This is an example'

    def setupQuery(self):
        print('Connecting to cassandra...')
        cluster = Cluster()
        self.session = cluster.connect()

        self.session.execute(
            "CREATE KEYSPACE cmpe220KS "
            "WITH replication="
            "{'class':'SimpleStrategy','replication_factor':1}"
        )
        self.session.execute("USE cmpe220KS")
        self.session.execute('CREATE TABLE tbl'
                             '(col1 INT PRIMARY KEY, col2 MAP<TEXT, BLOB>)')
        with open('data/cat.JPG', 'rb') as img:
            self.img_blob = base64.b64encode(img.read()).decode('utf-8')
        self.session.execute(
            "INSERT INTO tbl (col1, col2) VALUES(1, {'cat': textAsBlob('%s')})" % self.img_blob
        )

    def endQuery(self):
        print('Closing...')
        self.session.execute("DROP KEYSPACE cmpe220KS")

    def runQuery(self):
        for i in range(100):
            self.session.execute(
                "UPDATE tbl SET col2 = col2 + {'cat_%d': textAsBlob('%s')} WHERE col1=1" % (i, self.img_blob)
            )
