from numpy import empty
from endpoints import *
from precision import *
import random

def GetBalance():
    return GeneralEndpoint("balance", "GETAuth", enableDump=False)["data"]

def GetMarket():
    response = GeneralEndpoint("market", "GET", enableDump=True)
    return response

def GetOpenOrders(market):
    return GeneralEndpoint(f"open_order?market_id={market}", "GETAuth", enableDump=False)["data"]

def CancelOrder(**payloadTypes):
    response = GeneralEndpoint("cancel_order", "POSTAuth", enableDump=False, **payloadTypes)
    print(response)
    return response

def GetOrderBook(market):
    response = GeneralEndpoint(f"order_book?market_id={market}", "GET", enableDump=False)["data"]

    best_bid = "0"
    best_ask = str(float("inf")) # Whatever value is highest - needs optimising

    # Sort orderbook to get best bid and best ask
    for i in response:
        if i.get("side") == "buy":
            if (i.get("price")) > best_bid:
                best_bid = i.get("price")
        elif i.get("side") == "sell":
            if (i.get("price")) < best_ask:
                best_ask = i.get("price")
    
    return float(best_bid), float(best_ask)

def ExecuteOrder(**payloadTypes):
    response = GeneralEndpoint("new_order", "POSTAuth", enableDump=False, **payloadTypes)
    #print(response)
    return response

def orderType(quantity=0, value_in_range=0, id=0):
    sell_order = {
        "market_id": "FBX-USDT",
        "type": "limit",
        "side": "sell",
        "time_in_force": "gtc",
        "client_order_id": f"{int(random.uniform(10000, 99999999))}",
        "limit_price": f"{value_in_range}",
        "quantity": f"{quantity}"
    }

    buy_order_limit = {
        "market_id": "FBX-USDT",
        "type": "limit",
        "side": "buy",
        "time_in_force": "fok",
        "client_order_id": f"{int(random.uniform(10000, 99999999))}",
        "limit_price": f"{value_in_range}",
        "quantity": f"{quantity}"
    }

    # Market buying is disabled for some token pairs
    buy_order_market = {
        "market_id": "FBX-USDT",
        "type": "market",
        "side": "buy",
        "time_in_force": "ioc",
        "client_order_id": f"{int(random.uniform(10000, 99999999))}",
        "quantity": f"{quantity}"
    }

    cancel_order = {
        "market_id": "FBX-USDT",
        "type": "cancel_order",
        "id": f"{id}"
    }

    return sell_order, buy_order_limit, buy_order_market, cancel_order

def MakeBalanceEven(best_bid):
    print("Balance Uneven. Submitting Order...")
    quantityDifference =  abs(CheckBalance() - 2500)
    buy_order_limit = orderType(quantityDifference, my_ceil((best_bid - 0.0002), 4))[1]
    ExecuteOrder(**buy_order_limit)
    print("Order Complete. Balance now even.")

def CheckBalance():
    balance = float(GetBalance()[2]["total"])
    return balance

def ErrorHandling(quantity):
    print("Conflict Type_ErrorCode: Submitting Order...")
    buy_order_limit = orderType(quantity)[1]
    ExecuteOrder(**buy_order_limit)
    print(f"Limit Buy Submitted for Amount@{quantity}")

def main():
    c = 0
    while (c != 2500):
        best_bid, best_ask = GetOrderBook("FBX-USDT")
        inital_balance = CheckBalance()
        
        # Decimal residue will occur if ceiling function not taken
        # No in-built numpy or math functions will let you specify decimal precision
        best_bid = my_ceil((best_bid + 0.0002), 4)
        best_ask = my_ceil((best_ask - 0.0002), 4)
        
        # Get random value between best_bid and best_ask
        value_in_range = round(random.uniform(best_bid, best_ask),4)

        # Will fail if minimum value is below threshold needed to execute
        quantity = round(random.uniform(35, 200),4)
        
        sell_order = orderType(quantity, value_in_range)[0]
        sell_response = ExecuteOrder(**sell_order)
        print(f"Ask: Amount@{quantity} Price@{value_in_range}")

        buy_order_limit = orderType(quantity, value_in_range)[1]
        buy_response = ExecuteOrder(**buy_order_limit)
        print(f"Bid: Amount@{quantity} Price@{value_in_range}")
        
        # Store balance after the trade
        current_balance = CheckBalance()

        # TODO: Check no open orders
        if len(GetOpenOrders("FBX-USDT")) != 0:
            print(GetOpenOrders("FBX-USDT"))
            print(sell_response["data"]["id"])
            print(buy_response["data"]["id"])
            CancelOrder(**orderType(quantity, id=int(sell_response["data"]["id"]))[3])
            CancelOrder(**orderType(quantity, id=int(buy_response["data"]["id"]))[3])

        # Check if order was not filled correctly
        if "errorCode" in buy_response:
            ErrorHandling(quantity)
            continue
        # Optimise using WebSockets
        # Check initial wallet balance is equal to current balance after execution.
        elif (inital_balance != current_balance):
            MakeBalanceEven(best_bid)
        c += 1
        # main()

if __name__ == '__main__':
    main()