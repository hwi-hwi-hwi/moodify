from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Spotify API Credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Endpoint to get a new access token
@app.route('/get-token', methods=['GET'])
def get_token():
    refresh_token = request.args.get("refresh_token")
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=token_data)
    response_data = response.json()
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
