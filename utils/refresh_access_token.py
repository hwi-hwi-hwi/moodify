import requests
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

def get_new_access_token():
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN
    }
    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    response = requests.post(url, data=data, auth=auth)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to refresh access token: {response.json()}")
