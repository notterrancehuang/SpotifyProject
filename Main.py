import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

cid = open("ClientID", 'r')
c_secret = open("ClientSecret", 'r')
redirect_url = open("RedirectURL", 'r')
# Authentication without user. General stats of Spotify
scope = "user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid,
                                               client_secret=c_secret,
                                               redirect_uri=redirect_url,
                                               scope=scope))

results = sp.current_user_recently_played()
