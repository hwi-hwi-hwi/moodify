import requests
from base64 import b64encode

# Spotify App의 Client ID와 Client Secret
CLIENT_ID = "5d8de8ebc1164c1f8c65441f44e1326c"
CLIENT_SECRET = "f0922066e5b64349a4b210b24333f34a"

# 받은 Authorization Code
AUTHORIZATION_CODE = "AQADB3i6nsAFaSkJd4lLP_qa9rMGPaQxjUyIyFJ1nWsbW7BWwd_Xuq3QP0FA52aDmwR1TZgvj8hSVjvukOTzVyj3qb5RUdViLKk0BbKSqv7ZMwPW6wbEvvkZhegPalKngtAdai41MIRLdozGsPUz9XIJKCVGycsPcDl5-YnmpHFY_Z4X-SxoHcKy1oN1fXozqNN3DD9FIWTdUmUNtuF4_IxAlYwJmFopa3JijS0KbAr5wa--iKsMPMs"

# Redirect URI
REDIRECT_URI = "http://localhost:8888/callback/"

# Spotify API의 Token 교환 엔드포인트
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Base64로 Client ID와 Client Secret 인코딩
auth_header = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

# 요청 데이터
data = {
    "grant_type": "authorization_code",
    "code": AUTHORIZATION_CODE,
    "redirect_uri": REDIRECT_URI
}

# 요청 헤더
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# POST 요청으로 Access Token과 Refresh Token 가져오기
response = requests.post(TOKEN_URL, data=data, headers=headers)
if response.status_code == 200:
    tokens = response.json()
    print("Access Token:", tokens["access_token"])
    print("Refresh Token:", tokens["refresh_token"])
else:
    print("Error:", response.status_code, response.text)
