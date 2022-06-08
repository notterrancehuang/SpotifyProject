AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "htpps://api.spotify.com/v1/"
SPOTIFY_GET_TOP_TRACKS_URL = "https://api.spotify.com/v1/me/top/tracks"
playlist_id = None
user_id = "br7u4dvozt4civyc5wyxdl5x6"
SPOTIFY_CREATE_PLAYLIST_URL = f"https://api.spotify.com/v1/users/{user_id}/playlists"
SPOTIFY_ADD_TO_PLAYLIST_URL = None
auth_url = "https://accounts.spotify.com/api/token"
redirect_url = open("RedirectURL", 'r').read()
CLIENT_ID = open("ClientID", 'r').read()
CLIENT_SECRET = open("ClientSecret", 'r').read()
scope = "user-top-read playlist-modify-public"


def get_spotify_add_to_playlist_url(playlist_id):
    playlist_url_id = playlist_id.split(":")[2]
    SPOTIFY_ADD_TO_PLAYLIST_URL = f"https://api.spotify.com/v1/playlists/{playlist_url_id}/tracks"
    return SPOTIFY_ADD_TO_PLAYLIST_URL


def get_spotify_create_playlist_url(user_id):
    SPOTIFY_CREATE_PLAYLIST_URL = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    return SPOTIFY_CREATE_PLAYLIST_URL
