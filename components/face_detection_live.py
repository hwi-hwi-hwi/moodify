import cv2
import numpy as np
from keras.models import load_model
import time
from flask_socketio import SocketIO

# 모델 및 설정
face_detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

# 모델 로드
face_detection = cv2.CascadeClassifier(face_detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# 웹캠 설정
camera = cv2.VideoCapture(0)
socketio = SocketIO()

def detect_emotion_live(socketio_instance):
    last_update_time = time.time()
    update_interval = 1.0
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

        if len(faces) > 0 and (current_time - last_update_time > update_interval):
            (x, y, w, h) = faces[0]
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = np.expand_dims(roi, axis=-1)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_classifier.predict(roi)[0]
            sad_index = EMOTIONS.index("sad")
            sad_probability = preds[sad_index]
            print(f"Sad Probability: {sad_probability}")  # 디버깅용 출력

            # Sad 감정 강조 로직
            if sad_probability > 0.2:
                current_emotion = "sad"
            elif abs(sad_probability - max(preds)) < 0.1:
                current_emotion = "sad"
            else:
                current_emotion = EMOTIONS[np.argmax(preds)]

            current_confidence = np.max(preds)
            last_emotion = current_emotion
            last_confidence = current_confidence
            last_update_time = current_time

            socketio_instance.emit("emotion_update", {
                "emotion": last_emotion,
                "confidence": float(last_confidence)
            })

        frame_height, frame_width = frame.shape[:2]
        text_position = (frame_width - 200, 30)
        cv2.putText(frame, "Press 'Q' to quit.", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Real-Time Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting... Pressed 'Q'")
            break

    camera.release()
    cv2.destroyAllWindows()
