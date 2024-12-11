from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from utils.spotify_credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Spotify API 인증
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify = Spotify(auth_manager=auth_manager)

# 감정별 플레이리스트 매핑
emotion_to_playlist = {
    "happy": "7nAQSpFAhpq5TghMaz1fOc",
    "sad": "0W71HrCQ3QGQpqTL0esbfo",
    "angry": "00RSVMgoMRNEcWY9Nijoxs",
    "disgust": "4RpQWv15MLxNMrutUpgMLr",
    "scared": "4KvDXHNt5mARFoinM77xjk",
    "surprised": "1n1cbbMpDzZYuLveqh6QkY",
    "neutral": "7nXPOjFbqw3tV4eX9HTEoY"
}

def get_recommendations(emotion):
    """
    감정에 따라 적합한 음악 추천
    """
    playlist_id = emotion_to_playlist.get(emotion)
    if not playlist_id:
        return {"error": f"No playlist found for emotion: {emotion}"}

    try:
        playlist = spotify.playlist(playlist_id, market=None)  # market=None으로 설정
        tracks = [
            {"name": track["track"]["name"], "artist": track["track"]["artists"][0]["name"]}
            for track in playlist["tracks"]["items"]
        ]
        return {"emotion": emotion, "tracks": tracks[:10]}  # 상위 10곡만 반환
    except Exception as e:
        print(f"Error fetching playlist {playlist_id} for emotion {emotion}: {e}")
        return {"error": f"Failed to fetch playlist for {emotion}. Error: {str(e)}"}
