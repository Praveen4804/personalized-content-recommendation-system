import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
SPOTIPY_CLIENT_ID = "d0573551956149b28a20c0c16073bfaf"
SPOTIPY_CLIENT_SECRET = "dbc000e74bee410da1db0446536d3b1d"

auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)


def search_music(song_name):

    try:
        results = sp.search(q=song_name, type='track', limit=12)

        songs = []

        for item in results['tracks']['items']:

            songs.append({
                "song": item['name'],
                "artist": item['artists'][0]['name'],
                "image": item['album']['images'][0]['url'],
                "url": item['external_urls']['spotify']
            })

        return songs

    except Exception as e:
        print("Spotify API error:", e)
        return []