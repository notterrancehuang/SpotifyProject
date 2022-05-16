import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = open("ClientID", 'r')
c_secret = open("ClientSecret", 'r')
# Authentication without user. General stats of Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=cid,
                                                      client_secret=c_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
