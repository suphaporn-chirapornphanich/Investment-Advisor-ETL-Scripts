import pandas as pd
import numpy as np


class StockETLPipeline:


   @staticmethod
   def calculate_risk_return_scatter_data(returns, weights, portfolio_returns):
       # Annualized return and volatility for each stock
       scatter_data = []


       for ticker in returns.columns:
           daily_ret = returns[ticker]
           ann_return = ((1 + daily_ret.mean()) ** 252) - 1
           ann_vol = daily_ret.std() * np.sqrt(252)
           scatter_data.append({
               "Ticker": ticker,
               "AnnualReturn": ann_return,
               "AnnualVolatility": ann_vol,
               "Type": "Stock"
           })


       # Portfolio metrics
       ann_return_p = ((1 + portfolio_returns.mean()) ** 252) - 1
       ann_vol_p = portfolio_returns.std() * np.sqrt(252)
       scatter_data.append({
           "Ticker": "Portfolio",
           "AnnualReturn": ann_return_p,
           "AnnualVolatility": ann_vol_p,
           "Type": "Portfolio"
       })


       return pd.DataFrame(scatter_data)


   @staticmethod
   def calculate_metrics(df, weights):
       df['Date'] = pd.to_datetime(df['Date'])
       pivot = df.pivot(index="Date", columns="Ticker", values="Close")
       returns = pivot.pct_change().dropna()


       # Portfolio weighted returns
       weighted_returns = returns.copy()
       for ticker, weight in weights.items():
           weighted_returns[ticker] *= weight / 100


       portfolio_returns = weighted_returns.sum(axis=1)
       portfolio_cumulative = (1 + portfolio_returns).cumprod()


       # === Create cumulative return for each stock ===
       cumulative_returns = (1 + returns).cumprod()
       cumulative_returns["Portfolio"] = portfolio_cumulative


       # Convert wide to long format for plotting
       cumulative_long = cumulative_returns.reset_index().melt(id_vars="Date", var_name="Ticker", value_name="CumulativeReturn")


       # === Financial Summary ===
       daily_volatility = portfolio_returns.std()
       annual_volatility = daily_volatility * np.sqrt(252)
       mean_daily_return = portfolio_returns.mean()
       annual_return = ((1 + mean_daily_return) ** 252) - 1
       sharpe_ratio = annual_return / annual_volatility
       rolling_max = portfolio_cumulative.cummax()
       drawdown = (portfolio_cumulative - rolling_max) / rolling_max
       max_drawdown = drawdown.min()
       n_days = (portfolio_returns.index[-1] - portfolio_returns.index[0]).days
       cagr = (portfolio_cumulative.iloc[-1]) ** (365 / n_days) - 1


       summary = pd.DataFrame({
           "Metric": [
               "Annual Return",
               "Annual Volatility",
               "Sharpe Ratio",
               "Max Drawdown",
               "CAGR"
           ],
           "Value": [
               annual_return,
               annual_volatility,
               sharpe_ratio,
               max_drawdown,
               cagr
           ]
       })


       # Fix: Use class method properly
       scatter_df = StockETLPipeline.calculate_risk_return_scatter_data(returns, weights, portfolio_returns)
       return cumulative_long, summary, scatter_df  # Returns 3 values

