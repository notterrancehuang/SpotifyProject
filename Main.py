import requests

SPOTIFY_GET_TOP_TRACKS_URL = "https://api.spotify.com/v1/me/top/tracks"
SPOTIFY_CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/br7u4dvozt4civyc5wyxdl5x6/playlists"
ACCESS_TOKEN = "BQBPI-SnMwtSA_2PDMaCbP58u8pOvJga7chFE5wJRg7F5bymgCJ3uuvoh-AxJT6CHJi6JcI3xb7P-erZCYnGPUn1imrdIx2rYHaY_TrAgxnkrc3uQow2pyuD1kAzQMyoDCxIEYQMyX7PyKD9cxlCaZoafKLOZoi4YDO4k4iHX57lobKinkvSm6_RLAhmFh8zzFJPunBM"
cid = open("ClientID", 'r')
c_secret = open("ClientSecret", 'r')
redirect_url = open("RedirectURL", 'r')
scope = "user-top-read playlist-modify-public"


def request_time_range():
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
    response = requests.get(
        SPOTIFY_GET_TOP_TRACKS_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        json={
            "limit": limit,
            "time_range": time_range
        }
    )
    json_response = response.json()

    return json_response


def create_playlist(name, public):
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        json={
            "name": name,
            "public": public
        }
    )
    json_response = response.json()

    return json_response


def main():
    # limit = input("How many items to return? ")
    # time_range = request_time_range()
    # top_plays = get_top_plays(limit, time_range)
    # print(f"Top plays: {top_plays}")

    playlist = create_playlist(
        name="New test playlist",
        public=True
    )
    print(f"Playlist: {playlist}")


if __name__ == "__main__":
    main()
