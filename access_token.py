import info
import requests
import base64
from dataclasses import dataclass


@dataclass
class AccessToken:
    def __init__(self):
        ccs = info.CLIENT_ID + ':' + info.CLIENT_SECRET

        auth_header = base64.b64encode(ccs.encode("ascii"))

        headers = {
            'Authorization': "Basic " + auth_header.decode(),
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            'grant_type': 'client_credentials',
        }

        access_token_request = requests.post(
            url=info.TOKEN_URL, data=payload, headers=headers)
        access_token_response_data = access_token_request.json()
        access_token = access_token_response_data["access_token"]
        
        self.ACCESS_TOKEN = access_token

    def get_access_token(self):
        return self.ACCESS_TOKEN
