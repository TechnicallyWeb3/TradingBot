import yfinance as yf
import pandas as pd

pd.set_option('mode.chained_assignment', None)

def get_stock_data(stock, period = 'max',interval = '1d', startdate = None, enddate = None):
        yf.pdr_override()
        df = yf.download(tickers=stock, start=startdate, end=enddate, interval=interval,period=period)
        df.reset_index(inplace=True) 
      
        return df