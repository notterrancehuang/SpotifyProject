import hashlib
import os
import re
import requests
import json
import base64
import info
import access_token
import authorize


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


def request_limit():
    limit = int(input("How many items to return? "))
    # 0 <= limit <= 50
    if limit < 0 or limit > 50:
        limit = 20
    return limit


def get_top_plays(access_token, limit, time_range):
    """
    limit: number of songs to return
    time_range: the time range of top songs

    return json object
    """
    # get tracks that the user plays the most
    print("Access token: " + access_token)
    headers = {"Authorization": "Bearer " + access_token}
    r = requests.get("https://api.spotify.com/v1/me/top/tracks?limit="+str(limit), headers=headers)
    print(r)
    if r.status_code != 200:
        try:
            return r.json()
        except:
            print("Error trying to get top plays: " + str(r.status_code))
    # response = requests.get(
    #     info.SPOTIFY_GET_TOP_TRACKS_URL,
    #     headers={
    #         "Authorization": f"Bearer {access_token}"
    #     },
    #     params={
    #         "limit": limit,
    #         "offset": 0,
    #         "time_range": time_range
    #     }
    # )
    # if response.status_code != 200:
    #     try:
    #         return response.json()
    #     except:
    #         print("Error trying to get top plays: " + str(response.status_code))




def create_playlist(access_token, public):
    """
    public: a boolean for if the new playlist is public

    returns json object
    """
    # create a new playlist
    name = input("What is the playlist called? ")
    response = requests.post(
        info.get_spotify_create_playlist_url(info.user_id),
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": name,
            "public": public
        }
    )
    if response.status_code != 201:
        try:
            return response.json()
        except:
            print("Error trying to create playlist: " + str(response.status_code))


def add_songs(access_token, playlist_id, songs):
    """
    playlist_id: the id of the playlist 
    songs: list of song uris
    """
    # takes in a list of song ids and adds them to playlist
    for song in songs:
        add_song_to_playlist(access_token, playlist_id, song)


def add_song_to_playlist(access_token, playlist_id, song_uri):
    """
    playlist_id: the id of the playlist
    song_uri: the song id

    returns json object
    """
    # adds an individual song to playlist
    add_to_playlist_url = info.get_spotify_add_to_playlist_url(playlist_id)
    response = requests.post(
        add_to_playlist_url,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params={
            "uris": song_uri
        }
    )
    if response.status_code != 201:
        try:
            return response.json()
        except:
            print("Error trying to add song to playlist: " + str(response.status_code))


def main():
    at = access_token.AccessToken()
    token = at.get_access_token(info.CLIENT_ID, info.CLIENT_SECRET, info.TOKEN_URL)
    print(token)
    authorize.authorize_user()
    limit = request_limit()
    time_range = request_time_range()

    top_plays = get_top_plays(token, limit, time_range)
    # create json file with top songs info
    # output_file = open("top_songs_output.json", "w")
    # output_file.write(json.dumps(top_plays))
    # output_file.close()
    # songs_uri = []
    # for i in range(limit):
    #     songs_uri.append(top_plays["items"][i]["uri"])

    playlist = create_playlist(
        token, 
        public=True
    )
    # create json file with playlist info
    playlist_info = open("playlist_info.json", "w")
    playlist_info.write(json.dumps(playlist))
    playlist_info.close()

    playlist_id = playlist["uri"]
    print(playlist_id)

    add_songs(token, playlist_id, songs_uri)


if __name__ == "__main__":
    main()
