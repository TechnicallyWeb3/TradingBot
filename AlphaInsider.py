import requests
import json
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
api_key = os.getenv('ALPHAINSIDER_API')

# Define the API endpoints and parameters
BASE_URL = "https://alphainsider.com/api/"


HEADER = {
    "Authorization": f"Bearer {api_key}"
}
DEFAULT_LIMIT = 100
def getRequest(endpoint, params = None, body = None, header = None):
    url = BASE_URL + endpoint
    return requests.get(url, params=params, json=body, headers=header)

def postRequest(endpoint, params = None, body = None, header = None):
    url = BASE_URL + endpoint
    return requests.post(url, params=params, json=body, headers=header)
  
def getCategories(strategy_id) :
    params = {
        "strategy_id":strategy_id
    }
    return getRequest("getCategories", params = params)

def getOrders(strategy_id) :
    params = {
        "strategy_id":strategy_id
    }
    return json.loads(getRequest("getOrders", params = params, header = HEADER).content)['response']

def deleteOrder(strategy_id, order_id) :
    body = {
        "strategy_id":strategy_id,
        "order_id":order_id
    }
    return json.loads(postRequest("deleteOrder", body = body, header = HEADER).content)['response']

def deleteAllOrders(strategy_id) :
    orders = getOrders(strategy_id)
    for order in orders :
        order_id = order['order_id']
        deleteOrder(strategy_id, order_id)

def getPositions(strategy_id) :
    params = {
        "strategy_id":strategy_id
    }
    return json.loads(getRequest("getPositions", params = params, header=HEADER).content)['response']

def newPost(strategy_id, message = "", url = "") :
    body = {
        "strategy_id":strategy_id,
        "description":message,
        "url":url
    }
    return postRequest("newPost", body=body, header=HEADER)

def getPositionById(strategy_id, stock_id) :
    response = getPositions(strategy_id)
    for i in range(0, response.__len__()) :
        if response[i]['stock_id'] == stock_id :
            return response[i] #returns position data if exists
    return None #returns none if position doesn't exist

def positionExists(strategy_id, stock_id) :
    if getPositionById(strategy_id, stock_id) is not None :
        return True
    else :
        return False

def getPositionBalance(strategy_id, stock_id) :
    position_exists = positionExists(strategy_id, stock_id)

    if  position_exists:
        position = getPositionById(strategy_id, stock_id)
        return float(position['amount'])
    else : 
        return 0

def buyPosition(strategy, stock_id, total) :
    body = {
        "strategy_id":strategy,
        "stock_id":stock_id,
        "type":"market",
        "action":"buy",
        "total":total
    }
    return postRequest("newOrder", body=body, header=HEADER)

def sellPosition(strategy, stock_id, amount) :
    body = {
        "strategy_id":strategy,
        "stock_id":stock_id,
        "type":"market",
        "action":"sell",
        "amount":amount
    }
    return postRequest("newOrder", body=body, header=HEADER)

def getStockHistory(stock_id, start=None, end=None, limit=DEFAULT_LIMIT) :
    print(f"Getting stock data for {stock_id}")
    params = {
        "stock_id":stock_id,
        "limit":limit
    }
    
    return getRequest("getStockPriceHistory", params = params).json()['response']
