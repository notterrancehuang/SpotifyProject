import info
import requests
import base64
from http_end_point import HttpEndPoint
from dataclasses import dataclass


@dataclass
class AccessToken:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base64_string = base64.urlsafe_b64encode(
            (self.client_id + ":" + self.client_secret).encode()).decode()
        self.token_api_url = "https://accounts.spotify.com/api/token"

    def get_access_token(self):
        """
        client_id: the client id
        client_secret: the client secret
        url: the url to get token
        """

        end_point = HttpEndPoint(
            api_url=self.token_api_url, auth_base64=self.base64_string)
        response = end_point.create_end_point()
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception("Cannot get access token! - " +
                            response.json()['error'])

        # ccs = client_id + ':' + client_secret

        # auth_header = base64.b64encode(ccs.encode("ascii"))

        # headers = {
        #     'Authorization': "Basic " + auth_header.decode(),
        #     "Content-Type": "application/x-www-form-urlencoded"
        # }

        # payload = {
        #     'grant_type': 'client_credentials',
        # }

        # access_token_request = requests.post(
        #     url=url, data=payload, headers=headers)
        # access_token_response_data = access_token_request.json()
        # access_token = access_token_response_data["access_token"]

        # # return access_token
        # return \
        #     "BQA1RVokjJ1knKwtbeAi8BM2_tkDs4tLPqAxJbnOyS87OOdK0n_XNa8pDgnF7O5MagrQFicgeuQSmr25dHMCeOPBCOgMnyxSZ6yAPIsSygHQ0OVDRM60JNrPuF6EzJUZ9GKRMuESCwcWJEMn1k2cIw55PxBc4y6pbwUN3c82fqKFfjwZj_89NfQfykArgdknis13U2coON6uBJjHFnNu-pzr2L3LjB-lihUuvCY0w7n63SDMgy00vcv2FbBYRlY-6smefg"
