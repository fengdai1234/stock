from alpaca.trading.client import TradingClient
import os
import alpaca_trade_api as tradeapi
from backtesting_live import calculate_indicators
import time
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ['paper_key']
api_secret = os.environ['paper_secret']
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
trading_client = TradingClient(api_key, api_secret, paper=True)

# Getting account information and printing it
account = trading_client.get_account()
for property_name, value in account:
    print(f"\"{property_name}\": {value}")

# live trading:
SYMBOL = 'AAPL'
TIMEFRAME = '1Day'  # Adjust for real-time data
RSI_PERIOD = 14
EMA_FAST = 9
EMA_SLOW = 20
TRADE_QUANTITY = 1

# Function to fetch live data
def get_live_data(symbol, timeframe, limit=100):
    bars = api.get_bars(symbol, timeframe, limit=limit).df
    return bars

# Function to check positions
def get_position(symbol):
    try:
        position = api.get_position(symbol)
        return int(position.qty)
    except tradeapi.rest.APIError:
        return 0  # No position

# Function to execute trades
def execute_trade():
    # Fetch live data
    data = get_live_data(SYMBOL, TIMEFRAME)
    data = calculate_indicators(data)

    # Get the latest data row
    last_row = data.iloc[-1]

    # Check current position
    current_position = get_position(SYMBOL)

    # Buy condition
    if last_row['EMA9'] > last_row['EMA20'] and last_row['RSI'] > 30:
        if current_position == 0:  # No position, buy
            api.submit_order(
                symbol=SYMBOL,
                qty=TRADE_QUANTITY,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"Buy Order Placed at {last_row['close']:.2f}")

    # Sell condition
    elif last_row['EMA9'] < last_row['EMA20'] and last_row['RSI'] < 70:
        if current_position > 0:  # Position exists, sell
            api.submit_order(
                symbol=SYMBOL,
                qty=TRADE_QUANTITY,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print(f"Sell Order Placed at {last_row['close']:.2f}")

# Live trading loop
try:
    print("Starting live trading...")
    while True:
        execute_trade()
        time.sleep(60)  # Wait for the next minute to fetch new data
except KeyboardInterrupt:
    print("Live trading stopped.")
