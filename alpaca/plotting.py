
import mplfinance as mpf
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# --- Plot 1: plotting ---
# Create a figure with subplots
def plot_perf(data, SYMBOL):
    # Identify Buy/Sell Signals
    data['Buy_Signal'] = (data['EMA9'] > data['EMA20']) & (data['RSI'] > 30)
    data['Sell_Signal'] = (data['EMA9'] < data['EMA20']) & (data['RSI'] < 70)

    # Filter consecutive signals to only show reversals
    buy_signals = data[data['Buy_Signal']].index
    sell_signals = data[data['Sell_Signal']].index

    # Keep only the first buy signal after a sell signal and vice versa
    filtered_buy_signals = []
    filtered_sell_signals = []

    last_signal = None
    for i in data.index:
        if i in buy_signals and last_signal != 'Buy':
            filtered_buy_signals.append(i)
            last_signal = 'Buy'
        elif i in sell_signals and last_signal != 'Sell':
            filtered_sell_signals.append(i)
            last_signal = 'Sell'

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})

    # --- Plot 1: Candlestick Chart and EMAs ---
    data_for_candlestick = data[['open', 'high', 'low', 'close']]
    data_for_candlestick.index = pd.to_datetime(data.index)  # Ensure datetime index

    # Candlestick chart
    mpf.plot(
        data_for_candlestick,
        type='candle',
        ax=ax[0],
        style='yahoo',
        show_nontrading=True
    )

    # Plot EMAs
    ax[0].plot(data['EMA9'], label='EMA9', linestyle='--', color='orange', linewidth=1)
    ax[0].plot(data['EMA20'], label='EMA20', linestyle='--', color='purple', linewidth=1)

    # Plot filtered Buy/Sell signals
    ax[0].scatter(filtered_buy_signals, data.loc[filtered_buy_signals, 'close'], label='Buy Signal', marker='^', color='green', s=100)
    ax[0].scatter(filtered_sell_signals, data.loc[filtered_sell_signals, 'close'], label='Sell Signal', marker='v', color='red', s=100)

    # Titles and Labels
    ax[0].set_title(f'EMA + RSI Scalping Strategy for {SYMBOL}', fontsize=14, weight='bold')
    ax[0].set_ylabel('Price')
    ax[0].legend(loc='upper left')
    ax[0].grid(alpha=0.3)

    # Format x-axis for better readability
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax[0].xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax[0].tick_params(axis='x', rotation=45)

    # --- Plot 2: RSI ---
    ax[1].plot(data['RSI'], label='RSI', color='blue', alpha=0.8)
    ax[1].axhline(70, color='red', linestyle='--', alpha=0.5, label='Overbought (70)')
    ax[1].axhline(30, color='green', linestyle='--', alpha=0.5, label='Oversold (30)')

    # Titles and Labels
    ax[1].set_title('Relative Strength Index (RSI)', fontsize=12)
    ax[1].set_ylabel('RSI')
    ax[1].set_xlabel('Date')
    ax[1].legend(loc='upper left')
    ax[1].grid(alpha=0.3)

    # Format x-axis for RSI subplot
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax[1].xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax[1].tick_params(axis='x', rotation=45)

    # Tight layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.show()
