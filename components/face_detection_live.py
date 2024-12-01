import sys
import os
import cv2
import numpy as np
from keras.models import load_model
from utils.mock_data import mockSongs  # 음악 데이터를 가져옴
import time

# 경로 설정
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
face_detection_model_path = os.path.join(base_dir, 'haarcascade_files', 'haarcascade_frontalface_default.xml')
emotion_model_path = os.path.join(base_dir, 'models', '_mini_XCEPTION.102-0.66.hdf5')

# 감정 목록
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

# 모델 로드
face_detection = cv2.CascadeClassifier(face_detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# 최근 감정 저장
last_emotion = None
last_confidence = 0.0
last_update_time = 0
update_interval = 0.5  # 감정 업데이트 간격 (초)

# 텍스트 표시 위치 설정
text_x, text_y = 10, 30  # 초기 텍스트 출력 위치
line_spacing = 30  # 텍스트 줄 간격

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

    # faces 배열이 비어 있지 않은지 확인
    if len(faces) > 0 and (time.time() - last_update_time > update_interval):
        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = np.expand_dims(roi, axis=-1)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_classifier.predict(roi)[0]
            emotion = EMOTIONS[np.argmax(preds)]
            confidence = np.max(preds)

            # 감정과 신뢰도 업데이트
            last_emotion = emotion
            last_confidence = confidence
            last_update_time = time.time()

            break  # 가장 큰 얼굴만 처리

    # 화면에 감정과 추천 노래 표시
    if last_emotion:
        recommended_songs = mockSongs.get(last_emotion, [])
        recommended_text = ", ".join([song['title'] for song in recommended_songs[:3]])  # 상위 3곡만 표시

        # 텍스트 출력
        texts = [
            f"Emotion: {last_emotion} ({last_confidence:.2f})",
            f"Recommended Songs: {recommended_text}",
        ]
        for i, text in enumerate(texts):
            cv2.putText(frame, text, (text_x, text_y + i * line_spacing),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # 얼굴에 사각형 표시
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Real-Time Emotion Detection with Music", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
