import requests
import pandas as pd
import time
import hmac
import hashlib
import json

# HashKey Global API Credentials
API_KEY = 'your_hashkey_api_key'
SECRET_KEY = 'your_hashkey_secret_key'
BASE_URL = 'https://api.hashkey.com'

def get_server_time():
    response = requests.get(f'{BASE_URL}/v1/public/time')
    return response.json()['serverTime']

def create_signature(parameters, secret_key):
    sorted_params = sorted(parameters.items())
    query_string = '&'.join([f"{key}={value}" for key, value in sorted_params])
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def get_market_data(symbol, interval='1h', limit=100):
    url = f'{BASE_URL}/v1/market/candles'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()['data']
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def calculate_bollinger_bands(df, window=20, num_std_dev=2):
    df['SMA'] = df['close'].rolling(window).mean()
    df['stddev'] = df['close'].rolling(window).std()
    df['upper_band'] = df['SMA'] + (df['stddev'] * num_std_dev)
    df['lower_band'] = df['SMA'] - (df['stddev'] * num_std_dev)
    return df

def calculate_moving_average(df, short_window=50, long_window=200):
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()
    return df

def place_order(symbol, side, quantity, price):
    endpoint = '/v1/orders'
    url = f'{BASE_URL}{endpoint}'
    timestamp = get_server_time()
    params = {
        'api_key': API_KEY,
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'price': price,
        'timestamp': timestamp
    }
    params['sign'] = create_signature(params, SECRET_KEY)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(params))
    return response.json()

def main():
    symbol = 'BTCUSDT'
    interval = '1h'
    quantity = 0.001  # Trade quantity
    while True:
        # Fetch market data
        df = get_market_data(symbol, interval)
        
        # Calculate Bollinger Bands and Moving Averages
        df = calculate_bollinger_bands(df)
        df = calculate_moving_average(df)
        
        # Generate trade signals
        latest_data = df.iloc[-1]
        previous_data = df.iloc[-2]
        
        if (latest_data['close'] < latest_data['lower_band']) and (latest_data['short_ma'] > latest_data['long_ma']):
            # Buy signal
            price = latest_data['close']
            print(f"Placing buy order for {symbol} at {price}")
            place_order(symbol, 'buy', quantity, price)
        elif (latest_data['close'] > latest_data['upper_band']) and (latest_data['short_ma'] < latest_data['long_ma']):
            # Sell signal
            price = latest_data['close']
            print(f"Placing sell order for {symbol} at {price}")
            place_order(symbol, 'sell', quantity, price)
        
        time.sleep(3600)  # Wait for the next interval

if __name__ == "__main__":
    main()
