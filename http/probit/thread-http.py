from asyncio import as_completed
from access_token import AccessToken
import time
import threading
import requests
import json
import concurrent.futures

def FetchNewAccessToken():
  return AccessToken()["access_token"]

def sell_order():
    url = "https://api.probit.com/api/exchange/v1/new_order"

    payload = {
        "market_id": "FBX-USDT",
        "type": "limit",
        "side": "sell",
        "quantity": "38",
        "time_in_force": "gtc",
        "limit_price": "0.0283"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {FetchNewAccessToken()}"
    }

    response = requests.post(url, json=payload, headers=headers)

    stringifed_response = json.loads(response.text)
    data = json.dumps(stringifed_response, indent=2)
    print(data)

def buy_order():
    url = "https://api.probit.com/api/exchange/v1/new_order"

    payload = {
        "market_id": "FBX-USDT",
        "type": "limit",
        "side": "buy",
        "quantity": "38",
        "time_in_force": "fok",
        "limit_price": "0.0283"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {FetchNewAccessToken()}"
    }

    response = requests.post(url, json=payload, headers=headers)

    stringifed_response = json.loads(response.text)
    data = json.dumps(stringifed_response, indent=2)
    print(data)

with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(4):
        executor.submit(sell_order)
        executor.submit(buy_order)
    #executor.submit(time.sleep(9))
    

# for _ in range(3):
#     t1 = threading.Thread(target=sell_order)
#     t2 = threading.Thread(target=buy_order)
#     t1.start()
#     t2.start()
