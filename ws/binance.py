
# wss://stream.binance.com:9443/ws/bnbbtc@depth.

import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(data["b"])

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print(close_msg)

def streamKLine(symbol, streamName):
    socket = f'wss://stream.binance.com:9443/ws/{symbol}{streamName}'
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)    
    ws.run_forever()

def __main__():
    streamKLine("btcusdt", "@bookTicker")

__main__()
