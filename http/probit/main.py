from numpy import empty
from endpoints import *
from precision import *
import random

def GetBalance():
    return GeneralEndpoint("balance", "GETAuth", enableDump=False).get("data", {})

def GetMarket():
    response = GeneralEndpoint("market", "GET", enableDump=True)
    return response

def GetOpenOrders(market):
    return GeneralEndpoint(f"open_order?market_id={market}", "GETAuth", enableDump=False).get("data", {})

def CancelOrder(**payloadTypes):
    response = GeneralEndpoint("cancel_order", "POSTAuth", enableDump=False, **payloadTypes)
    #print(response)
    return response

def GetOrderBook(market):
    response = GeneralEndpoint(f"order_book?market_id={market}", "GET", enableDump=False).get("data", {})

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

    # Market buying is disabled for some token pairs
    buy_order_market = {
        "market_id": "FBX-USDT",
        "type": "market",
        "side": "buy",
        "time_in_force": "ioc",
        "quantity": f"{quantity}"
    }

    cancel_order = {
        "market_id": "FBX-USDT",
        "type": "cancel_order",
        "id": f"{id}"
    }

    return sell_order, buy_order_limit, buy_order_market, cancel_order

def MakeBalanceEven(best_bid, best_ask):
    quantityDifference =  CheckBalance() - 2500
    quantityDifference = my_ceil(quantityDifference, 4)
    print(f"Balance Uneven. Submitting Order for {quantityDifference}...")

    if quantityDifference > 0:
        best_bid = my_ceil((best_bid - 0.0004), 4)
        print(best_bid)
        sell_order = orderType(quantityDifference, best_bid)[0]
        print(ExecuteOrder(**sell_order))
    elif quantityDifference < 0:
        best_ask = my_ceil((best_ask + 0.0004), 4)
        print(best_ask)
        buy_order_limit = orderType(abs(quantityDifference), best_ask)[1]
        print(ExecuteOrder(**buy_order_limit))
    
    print("Order Complete. Balance now even.")

def CheckBalance():
    balance = float(GetBalance()[2].get("total", "<total not found>"))
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
        sell_response_id = sell_response.get("data", {}).get("id", {})
        buy_response_id = buy_response.get("data", {}).get("id", {})

        # TODO: Check no open orders
        if len(GetOpenOrders("FBX-USDT")) != 0:
            print("Looks like someone else filled you. Cancelling orders...")
            CancelOrder(**orderType(quantity, id=sell_response_id)[3])
            CancelOrder(**orderType(quantity, id=buy_response_id)[3])

        # Check if order was not filled correctly
        if "errorCode" in buy_response:
            #print(quantity)
            #print(buy_response)
            ErrorHandling(quantity)
            # continue
        
        # Optimise using WebSockets
        # Check initial wallet balance is equal to current balance after execution.
        if (inital_balance != current_balance):
            MakeBalanceEven(best_bid, best_ask)
        c += 1
        # main()

if __name__ == '__main__':
    main()