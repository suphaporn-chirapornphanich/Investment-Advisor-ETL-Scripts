import yfinance as yf
import pandas as pd


def fetch_stock_data(tickers, period="6mo", interval="1d"):
   df_all = []
   for ticker in tickers:
       data = yf.Ticker(ticker).history(period=period, interval=interval)
       data["Ticker"] = ticker
       df_all.append(data)
   return pd.concat(df_all).reset_index()