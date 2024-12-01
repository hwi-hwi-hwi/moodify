import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
from keras.models import load_model
from utils.mock_data import mockSongs  # 음악 데이터를 가져옴

# 모델 경로와 감정 목록
face_detection_model_path = os.path.join(os.path.dirname(__file__), '..', 'haarcascade_files', 'haarcascade_frontalface_default.xml')
emotion_model_path = os.path.join(os.path.dirname(__file__), '..', 'models', '_mini_XCEPTION.102-0.66.hdf5')
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

# 모델 로드
face_detection = cv2.CascadeClassifier(face_detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# 웹캠 활성화
camera = cv2.VideoCapture(0)

print("Press 'q' to quit.")

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = np.expand_dims(roi, axis=-1)
        roi = np.expand_dims(roi, axis=0)

        preds = emotion_classifier.predict(roi)[0]
        emotion = EMOTIONS[np.argmax(preds)]
        confidence = np.max(preds)

        # 감정 결과와 음악 추천 표시
        recommended_songs = mockSongs.get(emotion, [])
        recommended_text = ", ".join([song['title'] for song in recommended_songs[:3]])  # 상위 3곡만 표시

        # 감정과 추천 음악 출력
        text = f"{emotion} ({confidence:.2f}) - Recommended: {recommended_text}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Real-Time Emotion Detection with Music", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
