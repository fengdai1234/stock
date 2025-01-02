import importlib
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import matplotlib.dates as mdates
import time
import plotting  # Import the module
from plotting import plot_perf
importlib.reload(plotting) 

from dotenv import load_dotenv
load_dotenv()
api_key = os.environ['paper_key']
api_secret = os.environ['paper_secret']

# Set your API credentials
base_url = 'https://paper-api.alpaca.markets'

# Instantiate the API client
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Fetch data for a specific date range
# Calculate RSI
def calculate_indicators(df):
    df['EMA9'] = df['close'].ewm(span=EMA_FAST, adjust=False).mean()
    df['EMA20'] = df['close'].ewm(span=EMA_SLOW, adjust=False).mean()
    
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=RSI_PERIOD).mean()
    avg_loss = pd.Series(loss).rolling(window=RSI_PERIOD).mean()
    
    rs = avg_gain / avg_loss
    RSI = 100 - (100 / (1 + rs))
    RSI.index = df.index
    df['RSI'] = RSI
    return df

def backtest_strategy(data, initial_balance=10000):
    balance = initial_balance
    position = 0
    trades = []

    for i in range(len(data)):
        # Buy condition
        if data['EMA9'].iloc[i] > data['EMA20'].iloc[i] and data['RSI'].iloc[i] > 30:
            if position == 0:  # Only buy if no position
                position = balance / data['close'].iloc[i]  # Buy shares
                balance = 0  # Use all balance
                trades.append({'Date': data.index[i], 'Type': 'Buy', 'Price': data['close'].iloc[i]})

        # Sell condition
        elif data['EMA9'].iloc[i] < data['EMA20'].iloc[i] and data['RSI'].iloc[i] < 70:
            if position > 0:  # Only sell if holding shares
                balance = position * data['close'].iloc[i]  # Sell all shares
                position = 0
                trades.append({'Date': data.index[i], 'Type': 'Sell', 'Price': data['close'].iloc[i]})

    # Calculate final balance
    final_balance = balance + (position * data['close'].iloc[-1] if position > 0 else 0)
    profit = final_balance - initial_balance

    return trades, final_balance, profit

# Backtesting function for Buy and Hold Strategy
def buy_and_hold(data, initial_balance=10000):
    start_price = data['close'].iloc[0]  # Buy at the first price
    end_price = data['close'].iloc[-1]  # Sell at the last price

    shares = initial_balance / start_price  # Number of shares purchased
    final_balance = shares * end_price  # Final balance after holding
    profit = final_balance - initial_balance

    return start_price, end_price, final_balance, profit


SYMBOL = 'AAPL'
TIMEFRAME = '1Day' 
start_date ='2024-01-02'
end_date ='2024-12-30'
EMA_FAST = 9
EMA_SLOW = 20
RSI_PERIOD = 14
data = api.get_bars(SYMBOL, TIMEFRAME, start=start_date, end=end_date).df
# Convert index to datetime if needed
data.index = pd.to_datetime(data.index)

# Filter for regular trading hours
# data = data.between_time('09:30', '16:00')
data = data[['open', 'high', 'low', 'close']]  # use 'close' prices only

data = calculate_indicators(data)

trades, strategy_final_balance, strategy_profit  = backtest_strategy(data)

# Backtest Buy and Hold Strategy
start_price, end_price, bh_final_balance, bh_profit = buy_and_hold(data)

# Display Results
print("=== Backtesting Results ===")
print(f"Initial Balance: $10000.00")

print("\n--- EMA + RSI Strategy ---")
print(f"Final Balance: ${strategy_final_balance:.2f}")
print(f"Profit: ${strategy_profit:.2f}")
print("Trade Log:")
for trade in trades:
    print(f"{trade['Date']}: {trade['Type']} at ${trade['Price']:.2f}")

print("\n--- Buy and Hold Strategy ---")
print(f"Start Price: ${start_price:.2f}")
print(f"End Price: ${end_price:.2f}")
print(f"Final Balance: ${bh_final_balance:.2f}")
print(f"Profit: ${bh_profit:.2f}")

# Compare Strategies
strategy_vs_bh = strategy_profit - bh_profit
if strategy_vs_bh > 0:
    print(f"\nYour strategy outperformed Buy and Hold by ${strategy_vs_bh:.2f}.")
else:
    print(f"\nBuy and Hold outperformed your strategy by ${-strategy_vs_bh:.2f}.")


# Plotting
plot_perf(data,'AAPL')
