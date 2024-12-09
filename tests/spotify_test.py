import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from utils.spotify_credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Spotify API 인증
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
spotify = Spotify(auth_manager=auth_manager)

# 테스트할 플레이리스트 ID
playlist_id = "7nAQSpFAhpq5TghMaz1fOc"  # 새 플레이리스트 ID

try:
    # 한국(KR) 시장에서 플레이리스트 가져오기
    playlist = spotify.playlist(playlist_id, market="KR")
    print("Playlist Name:", playlist["name"])
    print("Tracks:")
    for item in playlist["tracks"]["items"]:
        track = item["track"]
        print(f"- {track['name']} by {track['artists'][0]['name']}")
except Exception as e:
    print("Error:", e)
