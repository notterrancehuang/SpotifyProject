import requests
import json

SPOTIFY_GET_TOP_TRACKS_URL = "https://api.spotify.com/v1/me/top/tracks"
SPOTIFY_CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/br7u4dvozt4civyc5wyxdl5x6/playlists"
ACCESS_TOKEN = "BQAS321r3F5_b51-qqP3-1SqMUdgKNNYrujNrrtHRk8KDGx92K-bJHv7HLSl6z3-epbjruZ_xZ0qB-6RNU8QRLu8hE0B7n9b9ltiOr3U2SNJkJo1jUd96XwDCbfEXEvH8vb7WR5LvGLlwIpBBvkkyaVP3JFXK1KtNGJ2JrW8jJXxOWA14FJUN0H3F7aoCQJAr1tqL4MugHxzUmyfv_fUlqyHtYMu4JCinFgpGw"
cid = open("ClientID", 'r')
c_secret = open("ClientSecret", 'r')
redirect_url = open("RedirectURL", 'r')
scope = "user-top-read playlist-modify-public"


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
    limit = int(input("How many items to return? "))
    # 0 <= limit <= 50
    if limit < 0 or limit > 50:
        limit = 20
    time_range = request_time_range()

    top_plays = get_top_plays(limit, time_range)

    output_file = open("json_output.json", "w")
    output_file.write(json.dumps(top_plays))
    output_file.close()

    # playlist = create_playlist(
    #     name="New test playlist",
    #     public=True
    # )
    # print(f"Playlist: {playlist}")


if __name__ == "__main__":
    main()
