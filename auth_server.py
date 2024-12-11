import os
from flask import Flask, request, jsonify, redirect
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Spotify API 정보
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Flask 앱 설정
app = Flask(__name__)

@app.route("/")
def home():
    return "Spotify Auth Server is running!"

@app.route("/login")
def login():
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": "user-read-playback-state user-modify-playback-state"
    }
    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization code missing."}), 400

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    if response.status_code == 200:
        tokens = response.json()
        return jsonify(tokens)
    else:
        return jsonify({"error": response.json()}), response.status_code

@app.route("/get-token")
def get_token():
    refresh_token = request.args.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "Refresh token missing."}), 400

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    if response.status_code == 200:
        tokens = response.json()
        return jsonify(tokens)
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888, debug=True)