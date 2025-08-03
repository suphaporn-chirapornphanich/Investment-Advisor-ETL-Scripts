from extract import fetch_stock_data
from transform import StockETLPipeline

def main():
   tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
   df = fetch_stock_data(tickers)
   print(df)

if __name__ == "__main__":
   main()