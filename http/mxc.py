from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decouple import config

import requests
import json

# Save API credentials from .env to variables
ACCESS_KEY = config('ACCESS_KEY')
SECRET_KEY = config('SECRET_KEY')

# Establish endpoint
def appendEndpoint(endpoint, symbol):
  return (requests.Session(), 
  f'https://api.mexc.com{endpoint}', 
  {
    'symbol': symbol,
  },
  {
    'Accepts': 'application/json',
    'X-MEXC-APIKEY': ACCESS_KEY,
  })

# Read ask and bid prices from orderbooks
def readOrderBook(data):
  ask = data['asks'][0][0]
  bid = data['bids'][0][0]
  #print(json.dumps(data['asks'][0], indent=2))
  return float(ask), float(bid)

def calculateSpread(ask, bid):
  spread_abs = abs(ask - bid)
  spread_avg = (ask + bid)/2
  spread = (spread_abs / spread_avg) * 100
  spread_usd = ask - bid
  
  print(f"spread: {round(spread, 5)}%".format())
  print(f"spread_usd: ${round(spread_usd, 5)}".format())
  print("")

def main():
  getExchangeInfo = '/api/v3/exchangeInfo'
  getDepth = '/api/v3/depth'
  symbol = 'BTCUSDT'
  try:
    while (symbol != "helo"):
      (session, url, parameters, headers) = appendEndpoint(getDepth, symbol)
      response = session.get(url, params=parameters, headers=headers)
      data = json.loads(response.text)
      ask, bid = readOrderBook(data)
      calculateSpread(ask, bid)
    print(ask, bid)
    # print(json.dumps(data, indent=2))
  except (ConnectionError, Timeout, TooManyRedirects) as err:
    print(err)

main()

# PLAN (step by step)
# 1. Read current highest bid & ask price.
# 2. Set ask price to match bid price.
# 3. Send bid request.
# 4. Send ask request of exact bid request.
# NOTE: quantities should be random, given a range
