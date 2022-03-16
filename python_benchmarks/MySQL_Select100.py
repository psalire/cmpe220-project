'''
REQUIRED: have MySQL already running
docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=root-password123 -d mysql:8
pip install mysql-connector-python

(This is run from the parent directory, so
"python_benchmarks.AbstractBenchmark"
is required instead of "AbstractBenchmark")
'''
from python_benchmarks.AbstractBenchmark import AbstractBenchmark
import mysql.connector


class MySQL_Select100(AbstractBenchmark):

    def __init__(self):
        self.category = 'Read'
        self.description = 'This is an example'

    def setupQuery(self):
        print('Connecting to MySQL...')
        self.db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root-password123',
        )
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute("DROP DATABASE cmpe220db")
        except Exception as e:
            pass
        self.cursor.execute('CREATE DATABASE cmpe220db')
        self.cursor.execute('USE cmpe220db')
        self.cursor.execute(
            'CREATE TABLE fivecolumns('
            'col1 VARCHAR(14) PRIMARY KEY,'
            'col2 TEXT,'
            'col3 TEXT,'
            'col4 TEXT,'
            'col5 TEXT)'
        )
        for i in range(100):
            self.cursor.execute(
                "INSERT INTO fivecolumns(col1, col2, col3, col4, col5) "
                f"VALUES ('Rutuja_{i}', 'Palatkar', 'SJSU', 'Student', 'ID')"
            )

    def endQuery(self):
        # print('Closing...')
        # Delete database (also deletes table)
        self.cursor.execute("DROP DATABASE cmpe220db")

    def runQuery(self):
        for i in range(100):
            self.cursor.execute('SELECT * FROM fivecolumns')
            self.cursor.fetchall()
