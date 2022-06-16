import info
import requests
import base64
from dataclasses import dataclass


@dataclass
class AccessToken:
    def get_access_token(self, client_id, client_secret, url):
        """
        client_id: the client id
        client_secret: the client secret
        url: the url to get token
        """
        ccs = client_id + ':' + client_secret

        auth_header = base64.b64encode(ccs.encode("ascii"))

        headers = {
            'Authorization': "Basic " + auth_header.decode(),
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            'grant_type': 'client_credentials',
        }

        access_token_request = requests.post(
            url=url, data=payload, headers=headers)
        access_token_response_data = access_token_request.json()
        access_token = access_token_response_data["access_token"]
        
        return access_token
