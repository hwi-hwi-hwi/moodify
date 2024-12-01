# 얼굴 인식 코드
import cv2
import numpy as np

def detect_emotion(image):
    # 이미지 처리 및 얼굴 감정 분석 코드
    emotions = ['happy', 'sad', 'neutral', 'angry', 'surprised']
    return np.random.choice(emotions)  # 테스트용 랜덤 감정 반환
