import cv2
import numpy as np
from keras.models import load_model
import time
from flask_socketio import SocketIO

# 감정 및 모델 관련 설정
face_detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'  # 감지 모델 경로
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'  # 감정 분석 모델 경로
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

# 모델 로드
face_detection = cv2.CascadeClassifier(face_detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# 웹캠 설정
camera = cv2.VideoCapture(0)

# Flask-SocketIO 연결
socketio = SocketIO()

# 실시간 감정 분석 함수
def detect_emotion_live(socketio_instance):
    last_update_time = time.time()  # 마지막 업데이트 시간
    update_interval = 0.5  # 감정 분석 간격 (초)
    last_emotion = "N/A"
    last_confidence = 0.0

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame.")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        current_time = time.time()

        # 감정 분석 수행
        if len(faces) > 0 and (current_time - last_update_time > update_interval):
            (x, y, w, h) = faces[0]  # 첫 번째 얼굴만 처리
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = np.expand_dims(roi, axis=-1)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_classifier.predict(roi)[0]
            last_emotion = EMOTIONS[np.argmax(preds)]
            last_confidence = np.max(preds)

            last_update_time = current_time

            # 웹페이지로 감정 정보 송신
            socketio_instance.emit("emotion_update", {
                "emotion": last_emotion,
                "confidence": float(last_confidence)
            })

        # 영상 크기를 기준으로 우측 상단에 'Press Q to quit' 메시지 출력
        frame_height, frame_width = frame.shape[:2]
        text_position = (frame_width - 200, 30)  # 우측 상단 (X축 오른쪽에서 200px, Y축 30px)
        cv2.putText(frame, "Press 'Q' to quit.", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 얼굴에 사각형 표시
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 영상 출력
        cv2.imshow("Real-Time Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting... Pressed 'Q'")
            break

    camera.release()
    cv2.destroyAllWindows()
