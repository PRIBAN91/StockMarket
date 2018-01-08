from DataAccess.CassandraConn import session
import uuid
import sched
import time
import requests
import json
import statsmodels.api as sm

scheduler = sched.scheduler(time.time, time.sleep)
prepared_stmt = session.prepare("select distinct symbol from historical_spots")
row_list = session.execute(prepared_stmt)
symbol_list = []
for row in row_list:
    symbol_list.append(row.symbol)
arguments = ("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY",
             symbol_list, "15min", "compact", "XJ3VBRI216I7CZ9C")


def schedule_grab_from_api(interval, arguments):
    while True:
        grab_intraday_spots(*arguments)
        print "Grab completed at: " + str(time.time())
        time.sleep(interval * 60)


def grab_intraday_spots(URL, symbol_list, interval, output_size, api_key):
    for symbol in symbol_list:
        try:
            URL += "&symbol=" + symbol + "&interval=" + interval + "&outputsize=" + output_size + \
                   "&apikey=" + api_key
            response = requests.get(URL)
            raw_data = json.loads(response.text)['Time Series (' + interval + ')']
            sorted_data = sorted(raw_data)
            data = raw_data[sorted_data[len(sorted_data) - 1]]
            cql = "INSERT INTO intraday_spots (symbol, time_uuid, open, close, low, high, volume) VALUES" \
                  " (%s, %s, %s, %s, %s, %s, %s) USING TTL 86400;"
            session.execute(cql, (symbol, uuid.uuid1(), float(data["1. open"]), float(data["4. close"]),
                                  float(data["3. low"]), float(data["2. high"]), float(data["5. volume"])))
        except Exception as e:
            print "Exception while API call: " + str(e)

# schedule_grab_from_api(15, arguments)
