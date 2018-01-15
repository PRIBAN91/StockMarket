from DataAccess.CassandraConn import session
from cassandra.query import BatchStatement, ConsistencyLevel
from Utilities.RetryDecorator import retry
import csv
import datetime


def read_csv_to_cassandra(csv_path):
    with open(csv_path, "rb") as f_obj:
        reader = csv.reader(f_obj)
        batch, insert_statement = get_new_batch()
        symbol = ''
        for i, row in enumerate(reader):
            try:
                if i > 0:
                    if symbol != row[1]:
                        if i > 1:
                            execute_batch(batch)
                        symbol = row[1]
                        batch, insert_statement = get_new_batch()
                    batch.add(insert_statement, (row[1], datetime.datetime.strptime(row[0], "%Y-%m-%d"), float(row[2]),
                                                 float(row[3]), float(row[4]), float(row[5]), float(row[6])))
            except Exception as e:
                print "{} row has failed to insert because of the following Exception: {}".format(str(i), str(e))
                print " ".join(row)
        session.execute(batch)


@retry(Exception)
def execute_batch(batch):
    session.execute(batch)


def get_new_batch():
    insert_statement = session.prepare("INSERT INTO historical_spots (symbol, date_eod, open, close,"
                                       " low, high, volume) VALUES (?, ?, ?, ?, ?, ?, ?)")
    return BatchStatement(consistency_level=ConsistencyLevel.ONE), insert_statement

# Only one time usage
# read_csv_to_cassandra("C:\Users\prita\Downloads\RawData.csv")
