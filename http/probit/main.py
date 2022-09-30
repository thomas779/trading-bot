from queue import Empty
from endpoints import *
import json

import time

def GetBalance():
    response = GeneralEndpoint("balance", "GETAuth", enableDump=True)
    return print(response)

def GetMarket():
    response = GeneralEndpoint("market", "GET", enableDump=True)
    return print(response)

def GetTicker(market):
    response = GeneralEndpoint(f"ticker?market_ids={market}", "GET", enableDump=False)
    return response

def GetOrderBook(market):
    response = GeneralEndpoint(f"order_book?market_id={market}", "GET", enableDump=False)["data"]

    n = 0
    best_bid = "0"
    best_ask = GetTicker("FBX-USDT")["data"][0]["base_volume"] # Whatever value is highest

    for i in response:
        #print(response[n]["price"])
        #print(i.get("side"))
        if i.get("side") == "buy":
            if (i.get("price")) > best_bid:
                best_bid = i.get("price")
                #print(f'bid: {best_bid}')
        elif i.get("side") == "sell":
            if (i.get("price")) < best_ask:
                best_ask = i.get("price")
                #print(f'ask: {best_ask}')
        n += 1
    
    while True:
        print(f'bid: {float(best_bid)}')
        print(f'ask: {float(best_ask)}')
        time.sleep(5)

    jsonString = json.dumps(response)
    stringifed_response1 = json.loads(jsonString)
    data = json.dumps(stringifed_response1, indent=2)
    return print(data)
    return print(response)

def ReadOrderBook():
    response = GetOrderBook("FBX-USDT")
    pass

def main():
    #GetBalance()
    #GetMarket()
    GetOrderBook("FBX-USDT")

if __name__ == '__main__':
    main()