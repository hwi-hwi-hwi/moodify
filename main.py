from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from components.face_detection_live import detect_emotion_live

app = Flask(__name__)
socketio = SocketIO(app)

# 이벤트 상태 관리
thread = None
thread_stop_event = Event()

@app.route("/")
def index():
    return render_template("index.html")

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

if __name__ == "__main__":
    socketio.run(app, debug=True)
