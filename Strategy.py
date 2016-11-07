"""
Program Descriptions 
"""
import logging
from datetime import datetime
from BitCoin import BitCoin
import time
__author__ = 'Drew.gotbaum'
__date__ = '11/3/2016'
__version__ = '1.0'
__copyright__ = 'The Oakleaf Group, LLC.'


def log(message):
    print message
    logging.info(message)


class Status(object):
    SHORT = 'SHORT'
    """This is the flag used for indicating a short."""

    BUY = 'BUY'
    """This is a flag indicating a buy"""

    ACTIVE = 'ACTIVE'
    """This shows us if we have not bought/shorted yet."""

    CLOSED = 'CLOSED'
    """Indicates the end of the run."""


class Strategy(object):

    def __init__(self, lookback='2016-09-01', std_mult =1.5, intervals_til_close=20):
        self.bitcoin = BitCoin(lookback)
        """BitCoin data structure for handling price calls and storage"""
        self.status = Status.ACTIVE
        logging.basicConfig(filename='logs/StrategyRuns.log',
                            level=logging.INFO,
                            format='%(asctime)s, %(message)s',
                            datefmt='[%m/%d/%Y %H:%M]')
        self.open_price = 0
        self.close_price = 0
        self.intervals_to_close = intervals_til_close
        self.std_mult = std_mult
        self.run_file = 'runs/runs.txt'
        self.current_run = self.get_current_run()

    def close(self):
        """
        1. Calculates the profit.
        2. Calculates the minutes of the run
        3. Outputs stats to file.
        """

        # Calculate Profit
        if self.status == Status.SHORT:
            profit = self.open_price - self.close_price
        elif self.status == Status.BUY:
            profit = self.close_price - self.open_price
        else:
            raise TypeError('Close was called but short or buy flag not active.')

        # Calculate DateRange
        minutes = (datetime.now() - self.bitcoin.start_time).seconds / 60

        # Output to Stats
        runstats = open('logs/run_stats.txt', 'a')
        runstats.write('%d,%d,%d,%f,%s' %(self.current_run,
                                                                    self.bitcoin.interval,
                                                                    minutes,
                                                                    profit,
                                                                    self.status))
        runstats.close()

        self.status = Status.CLOSED
        log('%d,%s,%d,%f' %(self.current_run, self.status, self.bitcoin.interval,self.bitcoin.last_price))

    def get_current_run(self):
        """
        This opens the run file to get the last run number,
        increments it and saves file, then returns new run number
        :return:
        :rtype:
        """

        f = open(self.run_file, 'r')
        last_run = int(f.readline())
        f.close()

        current_run = last_run + 1
        out = open(self.run_file, 'w')
        out.write(str(current_run))
        out.close()
        return current_run

    def update_interval(self):
        price = self.bitcoin.current_price()
        if self.status == Status.ACTIVE: # If active check price to open
            if price >= (self.bitcoin.average_hist_price() +
                             (self.std_mult * self.bitcoin.std_hist_price())):
                self.status = Status.SHORT
                self.open_price = price
            elif price <= (self.bitcoin.average_hist_price() -
                             (self.std_mult * self.bitcoin.std_hist_price())):
                self.status = Status.BUY
                self.open_price = price
        else: # If trading check price to close
            if self.intervals_to_close == 0:
                return True
            else:
                self.intervals_to_close -= 1
                return False

    def run(self):
        """
        Check if __current_interval__ is more than a minute past:
            _True_ - sleep until minute past.
            _False_ - run __update_interval__
        If __update_interval__ returns a transaction value:
            _True_ - set the buy/short price and the correponding sell/buy price.
            _False_ - sleep for another minute

        """
        active = True
        while active:
            current_time = datetime.now()
            time_dif = (current_time - self.bitcoin.current_interval).seconds
            if time_dif < 60:
                time.sleep(60 - time_dif)
            close = self.update_interval()
            log('%d,%s,%d,%f' %(self.current_run, self.status, self.bitcoin.interval,self.bitcoin.last_price ))

            if close:
                self.close()
                active = False


def main():
    mult = 2
    intervals_til_close = 10
    lookback='2016-10-31'

    strat = Strategy(lookback=lookback, std_mult=mult, intervals_til_close=intervals_til_close  )
    strat.run()

if __name__ == '__main__':
    main()









