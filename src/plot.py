import matplotlib.pyplot as plt
import plotly.express as px
import os


def plot_cumulative_returns_matplotlib(df, output_dir="plots"):
   os.makedirs(output_dir, exist_ok=True)
   plt.figure(figsize=(10, 6))
   plt.plot(df['Date'], df['CumulativeReturn'], label="Cumulative Return")
   plt.title("Cumulative Portfolio Return")
   plt.xlabel("Date")
   plt.ylabel("Return")
   plt.grid(True)
   plt.legend()
   plt.tight_layout()
   plt.savefig(os.path.join(output_dir, "cumulative_return_matplotlib.png"))
   plt.close()


def plot_cumulative_returns_plotly(df, output_dir="plots"):
   os.makedirs(output_dir, exist_ok=True)
   fig = px.line(df, x='Date', y='CumulativeReturn', title="Cumulative Portfolio Return (Interactive)")
   fig.write_html(os.path.join(output_dir, "cumulative_return_plotly.html"))


def plot_comparison_plotly(df_long, output_dir="plots"):
   os.makedirs(output_dir, exist_ok=True)
   fig = px.line(df_long, x='Date', y='CumulativeReturn', color='Ticker',
               title="Cumulative Returns: Portfolio vs Individual Stocks")
   fig.write_html(os.path.join(output_dir, "compare_portfolio_plotly.html"))


def plot_comparison_matplotlib(df_long, output_dir="plots"):
   os.makedirs(output_dir, exist_ok=True)
   plt.figure(figsize=(12, 6))
   for ticker in df_long["Ticker"].unique():
       ticker_df = df_long[df_long["Ticker"] == ticker]
       plt.plot(ticker_df["Date"], ticker_df["CumulativeReturn"], label=ticker)
   plt.title("Cumulative Returns: Portfolio vs Individual Stocks")
   plt.xlabel("Date")
   plt.ylabel("Cumulative Return")
   plt.legend()
   plt.grid(True)
   plt.tight_layout()
   plt.savefig(os.path.join(output_dir, "compare_portfolio_matplotlib.png"))
   plt.close()


def plot_risk_return_scatter_plotly(scatter_df, output_dir="plots"):
   import plotly.express as px
   os.makedirs(output_dir, exist_ok=True)
   fig = px.scatter(
       scatter_df,
       x="AnnualVolatility",
       y="AnnualReturn",
       color="Type",
       text="Ticker",
       title="Risk vs Return: Portfolio and Stocks",
       labels={"AnnualVolatility": "Volatility (Risk)", "AnnualReturn": "Annualized Return"},
   )
   fig.update_traces(textposition="top center")
   fig.write_html(os.path.join(output_dir, "risk_return_scatter_plotly.html"))


def plot_risk_return_scatter_matplotlib(scatter_df, output_dir="plots"):
   os.makedirs(output_dir, exist_ok=True)
   import matplotlib.pyplot as plt


   fig, ax = plt.subplots(figsize=(10, 6))
   for _, row in scatter_df.iterrows():
       color = "blue" if row["Type"] == "Stock" else "red"
       ax.scatter(row["AnnualVolatility"], row["AnnualReturn"], label=row["Ticker"], color=color)
       ax.text(row["AnnualVolatility"], row["AnnualReturn"], row["Ticker"], fontsize=9)
  
   ax.set_xlabel("Volatility (Risk)")
   ax.set_ylabel("Annualized Return")
   ax.set_title("Risk vs Return: Portfolio and Stocks")
   ax.grid(True)
   plt.tight_layout()
   plt.savefig(os.path.join(output_dir, "risk_return_scatter_matplotlib.png"))
   plt.close()



