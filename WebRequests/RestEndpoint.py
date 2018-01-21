# !/usr/bin/env python
import web
import json
from BusinessLogic.FetchArchivalSpots import FetchArchivalSpotDetails
from BusinessLogic.FetchIntradaySpots import FetchIntradaySpotDetails
from BusinessLogic.CalculateCorrelation import CalculateHistoricalCorrelation
from DataAccess.GrabIntradaySpots import symbol_list

urls = (
    '/index', 'index',
    '/GetArchivalSpot', 'fetch_historical_spots',
    '/GetIntradaySpot', 'fetch_intraday_spots',
    '/GetHistoricalCorrelation', 'fetch_historical_corr',
    '/favicon.ico', 'icon'
)

app = web.application(urls, globals())
render = web.template.render("../Resources/")


class index:
    def GET(self):
        return render.index("Home", "", symbol_list)


class fetch_historical_spots:
    def POST(self):
        data = json.loads(web.data())
        f = FetchArchivalSpotDetails(data['symbol'], data['start_date'], data['end_date'])
        result = f.get_user_requested_data()
        return json.dumps(result)


class fetch_intraday_spots:
    def POST(self):
        data = json.loads(web.data())
        f = FetchIntradaySpotDetails(data['symbol'])
        result = f.get_all_intraday_data()
        return json.dumps(result)


class fetch_historical_corr:
    def POST(self):
        data = json.loads(web.data())
        f = CalculateHistoricalCorrelation(data['symbol1'], data['symbol2'])
        result = f.calculate_correlation_for_pair()
        return json.dumps(result)


class icon:
    def GET(self):
        raise web.seeother("../Resources/favicon.ico")


if __name__ == "__main__":
    app.run()
