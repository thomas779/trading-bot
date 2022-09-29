from endpoints import *
import json

def GetBalance():
    response = GeneralEndpoint("balance", "GETAuth", enableDump=True)
    return print(response)

def GetMarket():
    response = GeneralEndpoint("market", "GET", enableDump=True)
    return print(response)

def GetTicker():
    response = GeneralEndpoint("ticker?market_ids=FBX-USDT", "GET", enableDump=True)["data"][]
    return print(response)

def main():
    #GetBalance()
    #GetMarket()
    GetTicker()

if __name__ == '__main__':
    main()