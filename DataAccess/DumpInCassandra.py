from DataAccess.CassandraConn import session
import csv


def read_csv_to_cassandra(csv_path):
    with open(csv_path, "rb") as f_obj:
        reader = csv.reader(f_obj)
        for i, row in enumerate(reader):
            if i > 0:
                try:
                    cql = "INSERT INTO historical_spots (symbol, date_eod, open, close," \
                          " low, high, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    session.execute(cql, (row[1], row[0], float(row[2]), float(row[3]), float(row[4]),
                                          float(row[5]), float(row[6])))
                    print "Successfully inserted row: " + str(i)
                except Exception as e:
                    print "{} row has failed to insert because of the following Exception: {}".format(str(i), str(e))
                    print " ".join(row)

# Only one time usage
# read_csv_to_cassandra("C:\Users\prita\Downloads\prices763fefc.csv")
