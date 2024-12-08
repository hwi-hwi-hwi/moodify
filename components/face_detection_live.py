import cv2
import numpy as np
from keras.models import load_model
import time
from collections import Counter
import platform

if platform.system() == "Windows":
    import win32gui
    import win32con

# 모델 및 설정
face_detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

# 모델 로드
face_detection = cv2.CascadeClassifier(face_detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

def set_window_topmost(window_name):
    """창을 항상 위로 설정"""
    if platform.system() == "Windows":
        hwnd = win32gui.FindWindow(None, window_name)
        if hwnd:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

def detect_emotion_live(socketio_instance):
    cap = cv2.VideoCapture(0)
    window_name = "Emotion Detection"
    cv2.namedWindow(window_name, cv2.WND_PROP_TOPMOST)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

    detection_results = []
    start_detection = False
    detection_start_time = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to access the webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 창을 항상 위로 설정
        set_window_topmost(window_name)

        # 초기 메시지 출력
        if not start_detection:
            cv2.putText(frame, "Press 'S' to start emotion detection", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'Q' to quit", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 감정 분석 시작
        if start_detection:
            elapsed_time = time.time() - detection_start_time

            if elapsed_time <= 5:  # 5초 동안 감정 분석
                countdown = 5 - int(elapsed_time)  # 카운트다운 계산
                cv2.putText(frame, f"Look at the camera for {countdown} seconds", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                for (x, y, w, h) in faces:
                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (64, 64))
                    face = face.astype("float") / 255.0
                    face = np.expand_dims(face, axis=-1)
                    face = np.expand_dims(face, axis=0)

                    predictions = emotion_classifier.predict(face)[0]
                    emotion = EMOTIONS[np.argmax(predictions)]
                    confidence = np.max(predictions)

                    detection_results.append({"emotion": emotion, "confidence": confidence})

                    # 실시간 감정 업데이트
                    socketio_instance.emit("emotion_update", {
                        "emotion": emotion,
                        "confidence": float(confidence)
                    })
            else:
                # 최종 감정 결과 계산 및 표시
                start_detection = False
                most_common_emotion = Counter([res["emotion"] for res in detection_results]).most_common(1)[0][0]
                avg_confidence = np.mean([res["confidence"] for res in detection_results if res["emotion"] == most_common_emotion])

                socketio_instance.emit("final_emotion", {
                    "emotion": most_common_emotion,
                    "confidence": float(avg_confidence)
                })

                # 최종 결과 메시지 표시
                cv2.putText(frame, "Emotion Detection Completed", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow(window_name, frame)  # 메시지 보여주기
                break  # 웹캠 창 종료

        # 얼굴에 사각형 그리기
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 영상 출력
        cv2.imshow(window_name, frame)

        # 키보드 입력 처리
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Q를 눌러 종료
            break
        elif key == ord('s') and not start_detection:  # S를 눌러 감정 분석 시작
            start_detection = True
            detection_start_time = time.time()

    cap.release()
    cv2.destroyAllWindows()
