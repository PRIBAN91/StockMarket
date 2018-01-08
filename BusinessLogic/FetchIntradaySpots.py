from DataAccess.CassandraConn import session
from cassandra import util


class FetchIntradaySpotDetails:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_all_intraday_data(self):
        results = []
        prepared_stmt = session.prepare("select * from intraday_spots where symbol = ?")
        bound_stmt = prepared_stmt.bind([self.symbol])
        db_results = session.execute(bound_stmt)
        for row in db_results:
            results.append({'timestamp': util.datetime_from_uuid1(row.time_uuid).__str__(), 'open': row.open,
                            'close': row.close, 'low': row.low, 'high': row.high, 'volume': row.volume})
        return results
