from fer import FER
import cv2
import numpy as np

# FER 기반 감정 인식 함수
def detect_emotion(image):
    # 이미지 디코딩
    frame = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

    # 감정 분석
    detector = FER(mtcnn=True)
    emotion, score = detector.top_emotion(frame)

    # 결과 반환
    if emotion:
        return {"emotion": emotion, "score": score}
    return {"error": "No emotion detected"}
