import requests
from requests import Response


class HttpEndPoint:
    def __init__(self, api_url: str, auth_base64: str):
        self.auth_base64_str = auth_base64
        self.url = api_url


    def create_end_point(self):
        header = {"Authorization": "Basic " + self.auth_base64_str, "Content-Type": "application/x-www-form-urlencoded"}
        payload = {"grant_type": "client_credentials"}
        session = requests.session()
        return session.post(self.url, headers=header, data=payload)