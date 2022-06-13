import info
import requests
import base64
from dataclasses import dataclass


@dataclass
class AccessToken:
    ACCESS_TOKEN = ""

    def get_access_token(self):
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
        
        return access_token
