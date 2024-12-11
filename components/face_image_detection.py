# 이미지로 받아서 감정 추출
import os
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

# 모델 경로 설정
MODEL_PATH = os.path.join(os.getcwd(), 'models', '_mini_XCEPTION.102-0.66.hdf5')
HAARCASCADE_PATH = os.path.join(os.getcwd(), 'haarcascade_files', 'haarcascade_frontalface_default.xml')

# 모델 및 Haarcascade 로드
emotion_classifier = load_model(MODEL_PATH, compile=False)
face_detection = cv2.CascadeClassifier(HAARCASCADE_PATH)

# 감정 레이블
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]


def detect_emotion(image):
    """
    이미지에서 얼굴을 감지하고 감정을 예측하는 함수.

    Args:
        image (werkzeug.datastructures.FileStorage): 업로드된 이미지 파일

    Returns:
        dict: 예측된 감정 및 확률 또는 오류 메시지
    """
    # 이미지 디코딩
    frame = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 감지
    faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        return {"error": "No face detected"}

    # 가장 큰 얼굴 선택
    (fX, fY, fW, fH) = faces[0]
    roi = gray[fY:fY + fH, fX:fX + fW]
    roi = cv2.resize(roi, (64, 64))  # 모델이 기대하는 크기인 64x64로 조정
    roi = roi.astype("float") / 255.0
    roi = np.expand_dims(roi, axis=-1)  # 채널 차원 추가 (64x64x1)
    roi = np.expand_dims(roi, axis=0)  # 배치 차원 추가 (1x64x64x1)

    # 감정 예측
    preds = emotion_classifier.predict(roi)[0]
    emotion = EMOTIONS[np.argmax(preds)]
    score = preds[np.argmax(preds)]

    return {"emotion": emotion, "score": float(score)}
