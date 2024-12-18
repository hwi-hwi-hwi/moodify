from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask import jsonify
from threading import Thread, Event
from components.face_detection_live import detect_emotion_live
from utils.data_loader import load_fer2013_data  # 데이터 로드 함수
from components.music_recommendation import get_recommendations
import os

app = Flask(__name__)
socketio = SocketIO(app)

# 데이터 로드
dataset_path = os.path.join(os.path.dirname(__file__), 'datasets', 'fer2013')
train_data, validation_data = load_fer2013_data(dataset_path)

# 데이터 확인
print("클래스 인덱스:", train_data.class_indices)
print("학습 데이터 샘플 수:", train_data.samples)
print("검증 데이터 샘플 수:", validation_data.samples)

# 이벤트 상태 관리
thread = None
thread_stop_event = Event()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend-music/<emotion>", methods=["GET"])
def recommend_music(emotion):
    """
    감정에 따라 추천 음악 반환
    """
    recommendations = get_recommendations(emotion)
    if "error" in recommendations:
        return jsonify(recommendations), 400  # 에러가 있으면 400 Bad Request 반환
    return jsonify(recommendations)

# WebSocket 이벤트 핸들러
@socketio.on("start_detection")
def handle_emotion_detection():
    global thread, thread_stop_event
    if thread is None or not thread.is_alive():
        thread_stop_event.clear()
        thread = Thread(target=detect_emotion_live, args=(socketio,))
        thread.start()
    else:
        emit("status", {"message": "Detection already running."})

@socketio.on("stop_detection")
def stop_emotion_detection():
    global thread_stop_event
    thread_stop_event.set()
    emit("status", {"message": "Detection stopped."})

if __name__ == "__main__":
    socketio.run(app, debug=True)
