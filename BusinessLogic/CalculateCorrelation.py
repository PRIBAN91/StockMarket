from DataAccess.CassandraConn import session
from collections import OrderedDict
import numpy as np

window_size = 500
decay_lambda = 0.98


class CalculateHistoricalCorrelation:
    def __init__(self, symbol1, symbol2):
        self.symbol1 = symbol1
        self.symbol2 = symbol2

    def calculate_correlation_for_pair(self):
        eod_dates, eod_spots1, eod_spots2 = self.compare_dates_and_clean()
        return_s1, return_s2 = [], []
        for idx in xrange(1, len(eod_dates), 1):
            return_s1.append(eod_spots1[idx] / eod_spots1[idx - 1] - 1)
            return_s2.append(eod_spots2[idx] / eod_spots2[idx - 1] - 1)
        decay_factors = self.calculate_entropy()
        hist_corr, dates_for_corr = [], []
        for idx in xrange(len(eod_dates) - 1, window_size, -1):
            dates_for_corr.append(eod_dates[idx])
            hist_corr.append(np.corrcoef(return_s1[idx - window_size:idx] * decay_factors,
                                         return_s2[idx - window_size:idx] * decay_factors)[0, 1])
        median_corr = np.percentile(hist_corr, 50)
        return {"median_corr": median_corr, "hist_dates": dates_for_corr, "hist_corr": hist_corr}

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

    @staticmethod
    def calculate_entropy():
        if decay_lambda == 1.0:
            return np.asarray([1.0] * window_size)
        else:
            return np.power(decay_lambda, np.linspace(window_size - 1, 0, window_size, endpoint=True))

# corr = CalculateHistoricalCorrelation('FFIV', 'YHOO')
# corr.calculate_return_and_entropy()
