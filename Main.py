import requests
import json
import base64

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "htpps://api.spotify.com/v1/"
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

# get access token
# TODO something is wrong with getting access token
auth_code = requests.get(AUTH_URL, {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": redirect_url,
    "scope": scope,
})

auth_header = base64.urlsafe_b64encode((CLIENT_ID + ":" + CLIENT_SECRET).encode())
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

payload = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": redirect_url,
}

access_token_request = requests.post(url=TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload, headers=headers)
access_token_response_data = access_token_request.json()
print(access_token_response_data)
ACCESS_TOKEN = access_token_response_data["access_token"]

# ACCESS_TOKEN = "BQAk5Y-ZaHC-5NdcGKz0rnuN50bkNES2GoH9lz14QhiTA_BPLD2RNYLr8WQ4QopgSqLwNr3zGQeThNwTBCRA3oOqHoGdripDjSXbJfIrd2EiI35z04_jeLeAl3h38zYnNrl_c1G2uBXapSyggEnE5TiDEN08MyEZKf_aBYaU0HCMLa2bMaLiT6Xxa0l28uYQRB0soqDYb9-jJ1Pdibf1JiGFn_DaMPAeUbM7Qg"

def request_time_range():
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
    # create a new playlist
    name = input("What is the playlist called? ")
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL,
        headers={ "Authorization": f"Bearer {ACCESS_TOKEN}" },
        json={
            "name": name,
            "public": public
        }
    )
    json_response = response.json()

    return json_response


def add_songs(playlist_id, songs):
    # takes in a list of song ids and adds them to playlist
    for song in songs:
        add_song_to_playlist(playlist_id, song)


def add_song_to_playlist(playlist_id, song_uri):
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
