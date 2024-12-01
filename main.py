from flask import Flask, render_template, request, jsonify
from components.face_detection import detect_emotion
from components.chat import handle_chat
from components.music_recommendation import recommend_music

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect-emotion', methods=['POST'])
def detect_emotion_route():
    image = request.files.get('image')
    emotion = detect_emotion(image)
    return jsonify({'emotion': emotion})

@app.route('/chat', methods=['POST'])
def chat_route():
    user_message = request.json.get('message')
    bot_response = handle_chat(user_message)
    return jsonify({'response': bot_response})

@app.route('/recommend-music', methods=['POST'])
def recommend_music_route():
    emotion = request.json.get('emotion')
    music_list = recommend_music(emotion)
    return jsonify({'music': music_list})

if __name__ == '__main__':
    app.run(debug=True)
