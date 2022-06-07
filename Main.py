import hashlib
import os
import re
import requests
import json
import base64

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "htpps://api.spotify.com/v1/"
ACCESS_TOKEN = None
SPOTIFY_GET_TOP_TRACKS_URL = "https://api.spotify.com/v1/me/top/tracks"
playlist_id = None
user_id = "br7u4dvozt4civyc5wyxdl5x6"
SPOTIFY_CREATE_PLAYLIST_URL = f"https://api.spotify.com/v1/users/{user_id}/playlists"
SPOTIFY_ADD_TO_PLAYLIST_URL = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
auth_url = "https://accounts.spotify.com/api/token"
redirect_url = open("RedirectURL", 'r').read()
CLIENT_ID = open("ClientID", 'r').read()
CLIENT_SECRET = open("ClientSecret", 'r').read()
scope = "user-top-read playlist-modify-public"


def get_access_token():
    ccs = CLIENT_ID + ':' + CLIENT_SECRET

    auth_header = base64.b64encode(ccs.encode("ascii"))

    headers = {
        'Authorization': "Basic " + auth_header.decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        'grant_type': 'client_credentials',
    }

    access_token_request = requests.post(
        url=TOKEN_URL, data=payload, headers=headers)
    access_token_response_data = access_token_request.json()
    print(access_token_response_data)
    ACCESS_TOKEN = access_token_response_data["access_token"]
    print("Access Token: " + ACCESS_TOKEN)


def authorize_user():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace("=", '')

    payload = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": scope,
        "redirect_uri": redirect_url,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }

    response = requests.get("https://accounts.spotify.com/authorize/?", params=payload)


def request_time_range():
    """
    Returns the time range string for get requests params to use
    """
    # what is the time frame that the top tracks are computed
    time_range_input = input("What is the time range?\n"
                             "\tShort-term is 4 weeks\n"
                             "\tMedium-term is 6 months\n"
                             "\tLong-term is several years\n"
                             "[s/m/l]: ").lower()
    if time_range_input == "s":
        return "short_term"
    elif time_range_input == "m":
        return "medium_term"
    elif time_range_input == "l":
        return "long_term"
    else:
        return "INVALID"


def get_top_plays(limit, time_range):
    """
    limit: number of songs to return
    time_range: the time range of top songs

    return json object
    """
    # get tracks that the user plays the most
    response = requests.get(
        SPOTIFY_GET_TOP_TRACKS_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        params={
            "limit": limit,
            "offset": 0,
            "time_range": time_range
        }
    )
    json_response = response.json()

    return json_response


def create_playlist(public):
    """
    public: a boolean for if the new playlist is public

    returns json object
    """
    # create a new playlist
    name = input("What is the playlist called? ")
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL,
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={
            "name": name,
            "public": public
        }
    )
    json_response = response.json()

    return json_response


def add_songs(playlist_id, songs):
    """
    playlist_id: the id of the playlist 
    songs: list of song uris
    """
    # takes in a list of song ids and adds them to playlist
    for song in songs:
        add_song_to_playlist(playlist_id, song)


def add_song_to_playlist(playlist_id, song_uri):
    """
    playlist_id: the id of the playlist
    song_uri: the song id

    returns json object
    """
    # adds an individual song to playlist
    response = requests.post(
        SPOTIFY_ADD_TO_PLAYLIST_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        params={
            "uris": song_uri
        }
    )
    json_response = response.json()

    return json_response


def main():
    get_access_token()
    authorize_user()
    limit = int(input("How many items to return? "))
    # 0 <= limit <= 50
    if limit < 0 or limit > 50:
        limit = 20
    time_range = request_time_range()

    top_plays = get_top_plays(limit, time_range)

    # create json file with top songs info
    output_file = open("top_songs_output.json", "w")
    output_file.write(json.dumps(top_plays))
    output_file.close()
    songs_uri = []
    for i in range(limit):
        songs_uri.append(top_plays["items"][i]["uri"])

    playlist = create_playlist(
        public=True
    )
    # create json file with playlist info
    playlist_info = open("playlist_info.json", "w")
    playlist_info.write(json.dumps(playlist))
    playlist_info.close()

    playlist_id = playlist["uri"]
    playlist_url_id = playlist["uri"].split(":")[2]
    print(playlist_id)
    SPOTIFY_ADD_TO_PLAYLIST_URL = f"https://api.spotify.com/v1/playlists/{playlist_url_id}/tracks"

    add_songs(playlist_id, songs_uri)


if __name__ == "__main__":
    main()
