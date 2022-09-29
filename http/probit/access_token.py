import requests
import base64
import json
from decouple import config

# Get OAUTH2 from the probit autists
def GetOAUTH2():
    ACCESS_KEY = config('CLIENT_ID')
    SECRET_KEY = config('CLIENT_SECRET')
    message = f'{ACCESS_KEY}:{SECRET_KEY}'
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = f'Basic {base64_bytes.decode("ascii")}'
    return base64_message

def AccessToken():
    url = "https://accounts.probit.com/token"

    payload = {"grant_type": "client_credentials"}
    headers = {
        "accept": "application/json",
        "Authorization": GetOAUTH2(),
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = json.loads(response.text)

    return data