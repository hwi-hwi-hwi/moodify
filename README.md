# Moodify 🎵 - Real-Time Emotion Detection & Music Recommendation System

**"Moodify"**는 사용자의 감정(Mood)을 분석하고, 그에 맞는 음악이나 플레이리스트를 추천하는 시스템입니다.  
이름은 **"Mood"**와 **"-ify"**의 결합으로, 감정을 음악으로 변환한다는 의미를 담고 있습니다.  
프로젝트의 목표는 딥러닝 기반의 감정 인식과 Spotify API를 활용한 음악 추천을 통해 사용자에게 새로운 경험을 제공하는 것입니다.

---

## 📌 프로젝트 개요
Moodify는 실시간 감정 분석과 음악 추천을 결합한 창의적인 프로젝트입니다.  
이 프로젝트는 사용자의 얼굴 표정을 기반으로 감정을 인식하고, 그 결과에 맞는 음악을 추천하는 시스템을 구현했습니다.

---

## 🌟 주요 기능

### 1. 실시간 감정 분석
- 사용자의 웹캠을 활용해 실시간으로 얼굴 표정을 분석.
- 사전에 학습된 CNN 기반 딥러닝 모델로 7가지 감정(Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral)을 분석.
- 결과를 그래프로 시각화하여 사용자가 직관적으로 확인 가능.

### 2. 음악 추천
- 감정 분석 결과를 기반으로 Spotify API를 통해 적합한 음악을 추천.
- 추천 창의 배경색은 최종 감정의 그래프 색상과 동기화되어 시각적 일관성을 제공합니다.

### 3. Spotify 연동
- Spotify Web Playback SDK를 사용해 음악을 직접 재생 가능.
- Spotify Web API를 통한 OAuth 2.0 인증으로 데이터 연동.

### 4. 사용자 친화적인 인터페이스
- 반응형 디자인을 통해 모바일 및 데스크톱 환경 모두 지원.
- 간단하고 직관적인 UI로 사용자 경험 최적화.

---

## 🛠️ 기술 스택 및 도구

- **프로그래밍 언어**: Python, JavaScript
- **프론트엔드**: HTML, CSS, Chart.js
- **백엔드**: Flask
- **라이브러리 및 프레임워크**: OpenCV, TensorFlow, Spotify Web Playback SDK
- **데이터셋**: FER2013 (감정 인식을 위해 사전 학습된 CNN 모델 사용)

---

## 🎯 프로젝트 개발 과정

### 1️⃣ 데이터 준비 및 모델 학습

#### 데이터셋: FER2013
- 7개 감정 클래스로 구성된 35,887개의 이미지.

#### 모델 설계: CNN 기반 감정 인식 모델
- 3개의 합성곱 레이어와 2개의 풀링 레이어, Dense 레이어를 활용.
- Dropout 비율 0.3으로 과적합 방지.

```python
# 모델 생성 예제
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def create_emotion_model(input_shape=(48, 48, 1), num_classes=7):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(num_classes, activation='softmax'))
    return model
```

#### 학습 및 개선
- **데이터 증강**: 이미지 회전, 이동, 확대, 뒤집기 적용.
- **클래스 불균형 처리**: class_weight 매개변수 사용.
- **평가 및 분석**: Confusion Matrix와 Classification Report로 성능 평가.

### 2️⃣ 기능 개발

#### 실시간 감정 분석
- OpenCV를 사용해 웹캠에서 입력된 이미지를 딥러닝 모델로 분석.
- 분석 결과를 실시간 그래프로 시각화.

#### 음악 추천
- 감정 분석 결과를 기반으로 Spotify API에서 추천 음악을 가져와 표시.
- 추천 창의 배경색을 그래프 색상과 동기화하여 감정을 반영.

---

## 🖥️ 사용 방법

### 1️⃣ 로컬 환경 설정
```bash
git clone https://github.com/hwi-hwi-hwi/moodify.git
cd moodify
pip install -r requirements.txt
```

### 2️⃣ Spotify API 설정
- Spotify Developer Dashboard에서 클라이언트 생성.
- `.env` 파일에 Client ID, Secret, Redirect URI 설정.

### 3️⃣ 앱 실행
```bash
python auth_server.py
python main.py
```

### 4️⃣ 사용 방법
1. **http://127.0.0.1:5000**에 접속.
2. Start Emotion Detection 버튼 클릭 → 실시간 감정 분석 시작.
3. 분석된 감정을 기반으로 추천 음악 확인 및 재생.

---

## 🛑 한계 및 개선점

### 1️⃣ Spotify API 프리미엄 계정 이슈
- Spotify Web Playback SDK는 프리미엄 계정에서만 작동.
- 테스트 과정에서 프리미엄 계정 인증 문제로 음악 재생 기능 완전 구현에 어려움이 있었음.

### 2️⃣ 채팅 기능 미구현
- 사용자 간 감정 및 음악 공유 기능은 시간 부족으로 제외.

### 3️⃣ 서버 배포 미완료
- 현재 로컬 환경에서만 테스트 완료.

---

### ✅ 테스트 방법
Moodify의 모바일 호환성을 직접 확인하려면 다음 단계를 따라주세요:

**Responsinator**에 접속.
URL 입력창에 로컬 서버 주소 또는 배포된 프로젝트 주소를 입력.
http://127.0.0.1:5000
Enter를 눌러 다양한 디바이스에서 Moodify의 작동을 확인.
## 📱 모바일 환경 지원
Moodify는 반응형 디자인을 채택하여 모바일 환경에서도 완벽하게 작동하도록 설계되었습니다.  
모바일 브라우저에서 감정 분석과 음악 추천 기능을 손쉽게 사용할 수 있습니다.

1. 첫 화면
![1  첫 화면](https://github.com/user-attachments/assets/ee52c7af-9965-4dee-b5d1-fdd3a9ca6011)


### ✅ 테스트 방법
1. **[Responsinator](http://www.responsinator.com/)**에 접속.
2. URL 입력창에 로컬 서버 주소 또는 배포된 프로젝트 주소를 입력.
   - `http://127.0.0.1:5000`
3. **Enter**를 눌러 다양한 디바이스에서 Moodify의 작동을 확인.

---

## 📚 참고 자료
- [FER2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)
- [Spotify Web Playback SDK Documentation](https://developer.spotify.com/documentation/web-playback-sdk)
- [Spotify Web API Authorization Guide](https://developer.spotify.com/documentation/web-api)
- [Responsinator for Mobile Testing](http://www.responsinator.com)

---

## 🏆 프로젝트 소감
이 프로젝트는 딥러닝, 음악 API 통합, 실시간 사용자 인터페이스 구현 등 기술적 도전을 포함하며, 창의적 사고를 요구했습니다.  
Moodify는 감정 분석과 음악 추천을 연결하는 혁신적인 접근을 통해 사용자 경험을 한 단계 발전시킬 가능성을 보여줬습니다. 🎧

---
