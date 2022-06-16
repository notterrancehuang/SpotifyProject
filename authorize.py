import base64
import re
import hashlib
import requests
import os
import info

def get_code_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace("=", '')

    return code_challenge


def authorize_user():
    payload = {
        "response_type": "code",
        "client_id": info.CLIENT_ID,
        "scope": info.scope,
        "redirect_uri": info.redirect_url,
        "code_challenge_method": "S256",
        "code_challenge": get_code_challenge(),
    }

    response = requests.get(
        "https://accounts.spotify.com/authorize/?", params=payload)