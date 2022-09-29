# wss://demo-api.probit.com/api/exchange/v1/ws

import websocket
import json

def on_message(ws, message):
    print(message)

def on_open(ws):
    msg = ({
    'type': 'subscribe',
    'channel': 'marketdata',
    'interval': 500,
    'market_id': 'FBX-USDT',
    'filter': ['ticker', 'order_books']
    })

    ws.send(json.dumps(msg))


websocket.enableTrace(True)
socket = 'wss://api.probit.com/api/exchange/v1/ws'
ws = websocket.WebSocketApp(socket)
ws.on_open = on_open
print(type(on_open))
ws.run_forever()