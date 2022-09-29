from access_token import AccessToken
import json
import requests

access_token = AccessToken()["access_token"]

def GeneralEndpoint(endpoint, submissionType, enableDump):
    url = f'https://api.probit.com/api/exchange/v1/{endpoint}'

    match submissionType:
        case "GET":
            headers = SetEndpointGET(endpoint)
        case "GETAuth":
            headers = SetEndpointGETAuthenticated(endpoint)
        case "POSTAuth":
            headers = SetEndpointPOSTAuthenticated(endpoint)
        case _:
            print("ERROR: submissionType")

    response = requests.get(url, headers=headers)

    if enableDump:
        stringifed_response = json.loads(response.text)
        data = json.dumps(stringifed_response, indent=2)
    else:
        data = json.loads(response.text)

    return data

# Set Endpoints for GET responses
def SetEndpointGET(endpoint):
    return {
        "accept": "application/json",
    }

# Set Endpoints for Authanticated GET responses
def SetEndpointGETAuthenticated(endpoint):
    return {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }

# Set Endpoints for authenticated POST requests
def SetEndpointPOSTAuthenticated(endpoint):
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }