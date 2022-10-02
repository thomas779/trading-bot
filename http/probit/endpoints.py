from os import access
from access_token import AccessToken
import json
import requests
import threading

def FetchNewAccessToken():
  return AccessToken()["access_token"]

# Endpoint expires after 15 mins
def GeneralEndpoint(endpoint, submissionType, enableDump, **payloadTypes):
    url = f'https://api.probit.com/api/exchange/v1/{endpoint}'

    match submissionType:
        case "GET":
            header = SetEndpointGET()
            response = requests.get(url, headers=header)
        case "GETAuth":
            header = SetEndpointGETAuthenticated()
            response = requests.get(url, headers=header)
        case "POSTAuth":
            payload, header = SetEndpointPOSTAuthenticated(**payloadTypes)
            response = requests.post(url, json=payload, headers=header)
            #print(requests.post(url, json=payload, headers=header))
        case _:
            print("ERROR: submissionType")

    if enableDump:
        stringifed_response = json.loads(response.text)
        data = json.dumps(stringifed_response, indent=2)
    else:
        data = json.loads(response.text)

    return data

# Set Endpoints for GET responses
def SetEndpointGET():
    return {
        "accept": "application/json",
    }

# Set Endpoints for Authanticated GET responses
def SetEndpointGETAuthenticated():
    return {
        "accept": "application/json",
        "authorization": f"Bearer {FetchNewAccessToken()}"
    }

# Set Endpoints for authenticated POST requests
def SetEndpointPOSTAuthenticated(**payloadTypes):
    if payloadTypes['type'] == "limit":
        payload = {
            "market_id": f"{payloadTypes['market_id']}",
            "type": f"{payloadTypes['type']}",
            "side": f"{payloadTypes['side']}",
            "time_in_force": f"{payloadTypes['time_in_force']}",
            "limit_price": f"{payloadTypes['limit_price']}",
            "quantity": f"{payloadTypes['quantity']}"
        }
    # Some markets may have market buying disabled
    elif payloadTypes['type'] == "market":
        payload = {
            "market_id": f"{payloadTypes['market_id']}",
            "type": f"{payloadTypes['type']}",
            "side": f"{payloadTypes['side']}",
            "time_in_force": f"{payloadTypes['time_in_force']}",
            "cost": f"{payloadTypes['quantity']}"
        }
    elif payloadTypes['type'] == "cancel_order":
        payload = {
            "market_id": f"{payloadTypes['market_id']}",
            "order_id": f"{payloadTypes['id']}"
        }
    else:
        print("ERROR: payload in POSTAuth")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {FetchNewAccessToken()}"
    }

    return payload, headers