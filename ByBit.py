import requests, json, datetime, hmac, hashlib, os
import pandas as pd
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BYBIT_KEY')
api_secret = os.getenv('BYBIT_SECRET')
TEST_URL = 'https://api-testnet.bybit.com/v5/'
BASE_URL = 'https://api.bybit.com/v5/'

GET_CANDLES = 'market/kline'
GET_TICKERS = 'market/tickers'
GET_ORDERS = 'order/realtime'
POST_ORDER = 'order/create'
POST_CANCEL_ALL = 'order/cancel-all'
GET_POSITIONS = 'position/list'
GET_ASSETS = 'asset/transfer/query-asset-info'

SPOT = 'spot'
MARKET_ORDER = 'Market'
BUY = 'Buy'
SELL = 'Sell'

DEFAULT_CHART = 'BTCUSDT'
DEFAULT_INTERVAL = '1'

def getRequest(endpoint, params = None, body = None, header = None):
    url = BASE_URL + endpoint
    return requests.get(url, params=params, json=body, headers=header).json()

def postRequest(endpoint, params = None, body = None, header = None):
    url = BASE_URL + endpoint
    return requests.post(url, params=params, json=body, headers=header)

def get_history(symbol = DEFAULT_CHART, category = SPOT, interval = DEFAULT_INTERVAL):
    get_params = {
    'category' : category,
    'symbol' : symbol,
    'interval' : interval
    }
    data = getRequest(GET_CANDLES, get_params)['result']['list']
    df = pd.DataFrame(data)
    df.columns = ['startTime', 'openPrice', 'highPrice', 'lowPrice', 'closePrice', 'volume', 'turnover']
    df = df.astype({'openPrice': float, 'highPrice': float, 'lowPrice': float, 'closePrice': float, 'volume': float})
    # Convert the startTime column to a datetime object
    df['startTime'] = pd.to_datetime(df['startTime'], unit='ms')

    df = df.rename(columns={'startTime': 'Date',
                        'openPrice': 'Open',
                        'highPrice': 'High',
                        'lowPrice': 'Low',
                        'closePrice': 'Close',
                        'volume': 'Volume',
                        'turnover': 'Turnover'})
    
    return df

def get_current(symbol = DEFAULT_CHART, category = SPOT) :
    get_params = {
    'category' : category,
    'symbol' : symbol
    }
    #if list data exists
    data = getRequest(GET_TICKERS, get_params)['result']['list']

    return data[0]
    #else return error

def get_price(symbol = DEFAULT_CHART) :
    return float(get_current(symbol)['lastPrice'])

def get_assets(coinName = None, timeStamp = int(datetime.datetime.now().timestamp()*1000)) :
    recv_window=str(5000)
    # Required
    get_params = {
        'accountType':'SPOT',
    }
    if coinName is not None:
        get_params['coin'] = coinName
        
    payload_str = urlencode(get_params)
    param_str= str(timeStamp) + api_key + recv_window + payload_str
    hash = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-TIMESTAMP': str(timeStamp),
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }

    return getRequest(GET_ASSETS, get_params, header=headers)

 