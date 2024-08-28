# HashKey-Global-CTA-bot
This is a Python trading bot using Bollinger Bands and Moving Averages to execute trades on the HashKey Global Exchange. The bot identifies potential buy and sell signals based on these technical indicators and places trades accordingly. Telegram: @ChildrenQ

## Requirements

- Python 3.7+
- `requests` library

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/hashkey-bollinger-ma-strategy.git
    cd hashkey-bollinger-ma-strategy
    ```

2. Install dependencies:

    ```bash
    pip install requests
    ```

## Usage

1. In the `strategy.py` file, fill in your API keys:

    ```python
    hashkey_api_key = 'YOUR_HASHKEY_API_KEY'
    hashkey_secret_key = 'YOUR_HASHKEY_SECRET_KEY'
    ```

2. Run the strategy:

    ```bash
    python strategy.py
    ```

## Strategy Overview

- **Bollinger Bands**: This strategy calculates the Bollinger Bands, a volatility indicator, to determine overbought or oversold conditions.
- **Moving Averages**: It uses a combination of short-term and long-term moving averages to confirm trends and potential entry/exit points.
- **Trade Execution**: When the price crosses the Bollinger Bands and moving averages signal a trend, the bot executes trades.
  
## Strategy Details

- **Initialization**: Set up API keys, fetch historical data, and compute Bollinger Bands and Moving Averages.
- **Signal Generation**: Monitor the price, and generate buy/sell signals based on the crossover of the price and moving averages with Bollinger Bands.
- **Execution**: Place orders on HashKey Global when signals are detected.

## Contribution

Feel free to submit issues and pull requests! Contact via Telegram: Telegram: @ChildrenQ
---
