from extract import fetch_stock_data
from load import save_to_csv
from plot import plot_cumulative_returns_matplotlib, plot_cumulative_returns_plotly, plot_comparison_matplotlib, plot_comparison_plotly
from plot import plot_risk_return_scatter_plotly, plot_risk_return_scatter_matplotlib
from transform import StockETLPipeline
import json
from datetime import datetime


# Load config
with open("config/portfolio_config.json") as f:
   config = json.load(f)


tickers = list(config["portfolio"].keys())
weights = config["portfolio"]


# Run ETL
df = fetch_stock_data(tickers)
# Fix: Unpack 3 values instead of 2
daily_returns, summary_stats, scatter_data = StockETLPipeline.calculate_metrics(df, weights)


# Save outputs
date_str = datetime.now().date().isoformat()
save_to_csv(daily_returns, f"data/portfolio_daily_{date_str}.csv")
save_to_csv(summary_stats, f"data/portfolio_summary_{date_str}.csv")
save_to_csv(scatter_data, f"data/scatter_data_{date_str}.csv")  # Save scatter data too


# Generate plots
plot_comparison_matplotlib(daily_returns)
plot_comparison_plotly(daily_returns)
plot_risk_return_scatter_matplotlib(scatter_data)  # Use scatter data
plot_risk_return_scatter_plotly(scatter_data)      # Use scatter data

