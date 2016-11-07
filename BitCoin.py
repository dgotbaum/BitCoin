"""
Program Descriptions 
"""
import pandas as pd
from exchanges.coindesk import CoinDesk
from datetime import datetime
from StringIO import StringIO
import urllib2
import gzip

__author__ = 'Drew.gotbaum'
__date__ = '11/3/2016'
__version__ = '1.0'
__copyright__ = 'The Oakleaf Group, LLC.'


class BitCoin(object):
    API = "http://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"

    def __init__(self, lookback):
        """
        Initialize the strategy by setting the initial lookback,
        populating the historical data, setting current interval,
        :param lookback: lookback date for historical data
        :type lookback: str
        """
        self.last_price = 0

        self.lookback = lookback
        """date to lookback for historical data."""

        self.current_interval = datetime.now()
        """This is the most recent interval that has been updated."""

        self.start_time = self.current_interval
        """Start time of the run."""

        self.historical = self._get_historical_df()
        """Dataset containing historical data."""

        self.interval = 1
        """This is the number of interval tracker to see how long this has gone on for."""

        self.data = self._populate_data()  # type: pd.DataFrame
        """Dataset containing minute data. [date, price, interval]"""

    def _get_historical_df(self):
        """
        Loads the historical data from CoinDesk
        :return: dataframe of historical data
        :rtype: pd.DataFrame
        """

        response = StringIO(urllib2.urlopen(self.API).read())
        string_csv = gzip.GzipFile(fileobj=response, mode='rb')
        df = pd.read_csv(string_csv, header=None, names=['ts','price','volume'])
        df['date'] = df.ts.apply(datetime.fromtimestamp)
        df = df[df.date > self.lookback]
        df = df.set_index('date')
        return df

    def _populate_data(self):
        """
        populate the initial interval of data
        :return: dataframe containing the current price
        :rtype: pd.DataFrame
        """
        now = datetime.now()
        price = float(CoinDesk.get_current_price(currency='USD'))
        df = pd.DataFrame([[now, price, self.interval]],
                            columns=['date', 'price', 'interval'],
                            )
        df = df.set_index('date')
        return df

    def current_price(self):
        """
        updates the interval and self.data with current price.

        :return: current price
        :rtype: float
        """
        now = datetime.now()
        self.interval += 1
        self.current_interval = now
        price = float(CoinDesk.get_current_price(currency='USD'))
        self.last_price = price
        self.data.ix[now] = [price, self.interval]
        return price

    def average_hist_price(self):
        return self.historical.price.mean()

    def std_hist_price(self):
        return self.historical.price.std()

    def average_price(self):
        return self.data.price.average()



