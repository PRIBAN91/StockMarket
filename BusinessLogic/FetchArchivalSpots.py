from DataAccess.CassandraConn import session
import datetime


class FetchArchivalSpotDetails:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") if start_date != "" else None
        self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") if end_date != "" else None

    def get_user_requested_data(self):
        if self.symbol is None or self.symbol == "":
            return []
        if self.start_date is None:
            return self.get_all_stock_data()
        if self.end_date is None:
            return self.get_data_from_start_date()
        return self.get_data_within_range()

    def get_all_stock_data(self):
        prepared_stmt = session.prepare("select * from historical_spots where symbol = ?")
        bound_stmt = prepared_stmt.bind([self.symbol])
        return self.prepare_result(bound_stmt)

    def get_data_from_start_date(self):
        prepared_stmt = session.prepare("select * from historical_spots where symbol = ? and date_eod >= ?")
        bound_stmt = prepared_stmt.bind([self.symbol, self.start_date])
        return self.prepare_result(bound_stmt)

    def get_data_within_range(self):
        prepared_stmt = session.prepare("select * from historical_spots where symbol = ? and date_eod >= ?"
                                        " and date_eod <= ? ")
        bound_stmt = prepared_stmt.bind([self.symbol, self.start_date, self.end_date])
        return self.prepare_result(bound_stmt)

    @staticmethod
    def prepare_result(bound_stmt):
        results = []
        db_results = session.execute(bound_stmt)
        for row in db_results:
            results.append({'timestamp': row.date_eod.__str__(), 'open': row.open, 'close': row.close,
                            'low': row.low, 'high': row.high, 'volume': row.volume})
        return results
