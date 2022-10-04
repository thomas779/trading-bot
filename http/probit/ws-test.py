import websocket
import json
from access_token import AccessToken

def on_message(ws, message):
    print ('message received ..')
    stringifed_response = json.loads(message)
    data = json.dumps(stringifed_response, indent=2)
    print(data)

def on_error(ws, error):
    print ('error happened .. ')
    print (error)


def on_close(ws):
    print ("### closed ###")

# Can't pass array into open_order?
def on_open(ws):
    open_order = str([{
        'market_id': 'FBX-USDT',
        'time_in_force': 'fok',
        'limit_price': '0.0267',
        'quantity': '12345',
        'side': 'sell',
        'type': 'limit'
    }])

    msg = ({
        'type': 'subscribe',
        'channel': f'{open_order}',
        })
    
    ws.send(json.dumps(msg))

websocket.enableTrace(True)
auth = f'Authorization: Bearer {AccessToken()["access_token"]}'
socket = 'wss://api.probit.com/api/exchange/v1/ws'
ws = websocket.WebSocketApp(socket,
                            on_open = on_open,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close,
                            header = [auth]
                            )
ws.on_open = on_open
print(type(on_open))
ws.run_forever()
    
    
    
