from DataAccess.CassandraConn import session
from collections import OrderedDict


class CalculateHistoricalCorrelation:
    def __init__(self, symbol1, symbol2):
        self.symbol1 = symbol1
        self.symbol2 = symbol2

    def calculate_return_and_entropy(self):
        eod_dates, eod_spots1, eod_spots2 = self.compare_dates_and_clean()
        print eod_dates, eod_spots1, eod_spots2

    def compare_dates_and_clean(self):
        d1 = self.fetch_close_spots(self.symbol1)
        d2 = self.fetch_close_spots(self.symbol2)
        common_dates = sorted(list(set(d1.keys()) & set(d2.keys())))
        cleaned_d1 = OrderedDict((k, d1[k]) for k in common_dates)
        cleaned_d2 = OrderedDict((k, d2[k]) for k in common_dates)
        return cleaned_d1.keys(), cleaned_d1.values(), cleaned_d2.values()

    @staticmethod
    def fetch_close_spots(symbol):
        prepared_stmt = session.prepare("select date_eod, close from historical_spots where symbol = ?")
        bound_stmt = prepared_stmt.bind([symbol])
        result = OrderedDict()
        db_results = session.execute(bound_stmt)
        for row in db_results:
            result[row.date_eod.__str__()] = row.close
        return result


# corr = CalculateHistoricalCorrelation('FFIV', 'YHOO')
# corr.calculate_return_and_entropy()
