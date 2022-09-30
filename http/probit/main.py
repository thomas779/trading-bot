from endpoints import *
from precision import *
import random

def GetBalance():
    return GeneralEndpoint("balance", "GETAuth", enableDump=False)["data"]

def GetMarket():
    response = GeneralEndpoint("market", "GET", enableDump=True)
    return print(response)

def GetTicker(market):
    response = GeneralEndpoint(f"ticker?market_ids={market}", "GET", enableDump=False)
    return response

def GetOrderBook(market):
    response = GeneralEndpoint(f"order_book?market_id={market}", "GET", enableDump=False)["data"]

    best_bid = "0"
    best_ask = str(float("inf")) # Whatever value is highest - needs optimising

    for i in response:
        if i.get("side") == "buy":
            if (i.get("price")) > best_bid:
                best_bid = i.get("price")
        elif i.get("side") == "sell":
            if (i.get("price")) < best_ask:
                best_ask = i.get("price")
    
    return float(best_bid), float(best_ask)

def ExecuteOrder(**payloadTypes):
    response = GeneralEndpoint("new_order", "POSTAuth", enableDump=True, **payloadTypes)
    #print(response)
    return response

def orderType(quantity, value_in_range=0):
    sell_order = {
        "market_id": "FBX-USDT",
        "type": "limit",
        "side": "sell",
        "time_in_force": "gtc",
        "limit_price": f"{value_in_range}",
        "quantity": f"{quantity}"
    }

    buy_order_limit = {
        "market_id": "FBX-USDT",
        "type": "limit",
        "side": "buy",
        "time_in_force": "fok",
        "limit_price": f"{value_in_range}",
        "quantity": f"{quantity}"
    }

    buy_order_market = {
        "market_id": "FBX-USDT",
        "type": "market",
        "side": "buy",
        "time_in_force": "ioc",
        "quantity": f"{quantity}"
    }

    return sell_order, buy_order_limit, buy_order_market

def MakeBalanceEven():
    current = []

    if float(GetBalance()[2]["total"]) != 2500:
        quantityDifference = float(GetBalance()[2]["total"]) - 2500
        buy_order_market = orderType(quantityDifference)[2]
        ExecuteOrder(**buy_order_market)
    current.append(float(GetBalance()[2]["total"]))
    current.append(float(GetBalance()[3]["total"]))
    
    return current

def main():
    c = 0
    while (c != 500):
        try:
            best_bid, best_ask = GetOrderBook("FBX-USDT")
            
            # Decimal residue will occur if ceiling function not taken
            # No in-built numpy or math functions will let you specify decimal precision
            best_bid = my_ceil((best_bid + 0.0002), 4)
            best_ask = my_ceil((best_ask - 0.0002), 4)
            
            # Get random value between best_bid and best_ask
            value_in_range = round(random.uniform(best_bid, best_ask),4)

            # Will fail if minimum value is below threshold needed to execute
            quantity = round(random.uniform(35, 750),4)
            
            sell_order = orderType(quantity, value_in_range)[0]
            response1 = ExecuteOrder(**sell_order)
            print(f"Ask: Amount@{quantity} Price@{value_in_range}")

            buy_order_limit = orderType(quantity, value_in_range)[1]
            response = ExecuteOrder(**buy_order_limit)
            print(f"Bid: Amount@{quantity} Price@{value_in_range}")
            
            # Optimise using WebSockets
            if "errorCode" in response:
                buy_order_market = orderType(quantity)[2]
                ExecuteOrder(**buy_order_market)
                print(f"Conflict Type_ErrorCode: Market Buy Completed. Amount@{quantity}")
                continue
            elif ((float(GetBalance()[2]["total"]) != MakeBalanceEven()[0])\
                & (float(GetBalance()[3]["total"]) != MakeBalanceEven()[1])):
                buy_order_market = orderType(quantity)[2]
                ExecuteOrder(**buy_order_market)
                # print("Very Sad. Someone else filled you.")
                print(f"Conflict Type_ExecuteOrder: Market Buy Completed. Amount@{quantity}")
                continue

            c += 1
            #time.sleep(0.5)
        except KeyError:
            print("KeyError captured. All good buddy.")
            continue

if __name__ == '__main__':
    main()
