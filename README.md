# Moodify 🎵 - Real-Time Emotion Detection & Music Recommendation System

"Moodify"는 사용자의 감정(Mood)을 분석하고, 그에 맞는 음악이나 플레이리스트를 추천하는 시스템입니다.  
이름은 "Mood"와 "-ify"의 결합으로, 감정을 음악으로 변환한다는 의미를 담고 있습니다.  
프로젝트의 목표는 딥러닝 기반의 감정 인식과 Spotify API를 활용한 음악 추천을 통해 사용자에게 새로운 경험을 제공하는 것입니다.

---

## 📌 프로젝트 개요
Moodify는 실시간 감정 분석과 음악 추천을 결합한 창의적인 프로젝트입니다.  
이 프로젝트는 사용자의 얼굴 표정을 기반으로 감정을 인식하고, 그 결과에 맞는 음악을 추천하는 시스템을 구현했습니다.

---

## 🌟 주요 기능

### 1. 실시간 감정 분석
- 사용자의 웹캠을 활용해 실시간으로 얼굴 표정을 분석합니다.
- 사전에 학습된 CNN 기반 딥러닝 모델로 7가지 감정(Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral)을 분석합니다.
- 결과를 그래프로 시각화하여 사용자가 직관적으로 확인 가능합니다.

### 2. 음악 추천
- 감정 분석 결과를 기반으로 Spotify API를 통해 적합한 음악을 추천합니다.
- 추천 창의 배경색은 최종 감정의 그래프 색상과 동기화되어 시각적 일관성을 제공합니다.

### 3. Spotify 연동
- Spotify Web Playback SDK를 사용해 플레이리스트를 직접 가져옵니다.
- Spotify Web API를 통한 OAuth 2.0 인증으로 데이터 연동합니다.

### 4. 사용자 친화적인 인터페이스
- 반응형 디자인을 통해 모바일 및 데스크톱 환경 모두 지원합니다.
- 간단하고 직관적인 UI로 사용자 경험 최적화합나다.

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
- 3개의 합성곱 레이어와 2개의 풀링 레이어, Dense 레이어를 활용합니다.
- Dropout 비율 0.3으로 과적합 방지합니다.
- 
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
- **데이터 증강**: 이미지 회전, 이동, 확대, 뒤집기 적용합니다.
- **클래스 불균형 처리**: `class_weight` 매개변수 사용합니다.
- **평가 및 분석**:
  - Confusion Matrix와 Classification Report로 각 감정 클래스에 대한 예측 정확도를 평가합니다다.
  - 아래 그래프는 모델 학습 동안의 훈련 정확도와 손실, 검증 정확도와 손실을 시각적으로 나타냅니다.

#### 모델 학습 성능 그래프:
![training_validation_plot3](https://github.com/user-attachments/assets/585147f1-c914-4f45-a87f-c70587a989a1)

- **Training vs Validation Accuracy**:
  - 그래프의 푸른 선은 훈련 데이터의 정확도(Training Accuracy)를 나타내고, 주황색 선은 검증 데이터의 정확도(Validation Accuracy)를 나타냅니다.
  - Epoch(학습 횟수)가 증가함에 따라 두 정확도가 점차 상승하고 수렴하는 모습을 보여줍니다.
  - 이는 모델이 안정적으로 학습되었음을 나타냅니다.

- **Training vs Validation Loss**:
  - 그래프의 푸른 선은 훈련 데이터의 손실(Training Loss)을 나타내고, 주황색 선은 검증 데이터의 손실(Validation Loss)을 나타냅니다.
  - Epoch가 진행될수록 손실 값이 감소하며 안정적인 모델 학습이 이루어졌음을 확인할 수 있습니다.

### 2️⃣ 기능 개발

#### 실시간 감정 분석
- OpenCV를 사용해 웹캠에서 입력된 이미지를 딥러닝 모델로 분석합니다.
- 분석 결과를 실시간 그래프로 시각화합니다.

#### 음악 추천
- 감정 분석 결과를 기반으로 Spotify API에서 추천 음악을 가져와 표시합니다.
- 추천 창의 배경색을 그래프 색상과 동기화하여 감정을 반영합니다.

---

## 🖥️ 사용 방법

### 1️⃣ 로컬 환경 설정
```bash
git clone https://github.com/hwi-hwi-hwi/moodify.git
cd moodify
pip install -r requirements.txt
```

### 2️⃣ Spotify API 설정
- Spotify Developer Dashboard에서 클라이언트 생성합니다.
- `.env` 파일에 Client ID, Secret, Redirect URI 설정합니다.

### 3️⃣ 앱 실행
```bash
python auth_server.py
python main.py
```

### 4️⃣ 사용 방법
1. **http://127.0.0.1:5000**에 접속합니다.
2. Start Emotion Detection 버튼 클릭 → 실시간 감정 분석을 시작합니다.
3. 분석된 감정을 기반으로 추천 음악 확인 및 재생합니다다.

---

### ✅ 테스트 방법

Moodify의 기능을 확인하려면 아래 단계를 따라주세요:

1. **로컬 서버 실행**  
   `python auth_server.py`와 `python main.py`를 실행하여 로컬 서버를 시작합니다.

2. **웹 브라우저 접속**  
   웹 브라우저에서 `http://127.0.0.1:5000`에 접속합니다.

3. **기능 테스트**  
   아래 단계에 따라 프로젝트 주요 기능을 테스트해보세요.

---

#### 💻 PC 환경

1️⃣ **첫 화면**  
- **Start Emotion Detection** 버튼을 클릭하면 웹캠 창이 실행됩니다.

![1 첫 화면](https://github.com/user-attachments/assets/ee52c7af-9965-4dee-b5d1-fdd3a9ca6011)

2️⃣ **카메라 동작**  
- **`S`**를 눌러 감정 인식을 시작합니다.  
- **`Q`**를 눌러 창을 닫을 수 있습니다 (X 클릭은 비활성화).

![2 카메라 실행](https://github.com/user-attachments/assets/0e3c77a2-6bf6-4acf-b6ff-7f1913b5b356)

3️⃣ **실시간 감정 보기**  
- 5초 동안 카메라를 응시하면 실시간으로 감지되는 감정과 신뢰도를 확인할 수 있습니다.  
- 그래프와 텍스트를 통 감정을 시각적으로 보여줍니다.

![3 카메라 보기](https://github.com/user-attachments/assets/bc2ba445-76c0-4328-a615-d2659259ea2f)

4️⃣ **결과 분석 및 음악 추천**  
- 감지된 감정에 따라 배경색과 그래프 색상이 동기화됩니다.
- 막대 그래프에 마우스를 가져가면 더 자세한 정보(신뢰도, 감지 빈도수)를 알 수 있습니다.
- 추천 음악 목록과 함께 재생 버튼이 표시됩니다.
- Start Emotion Detection 누르면 처음부터 다시 감정 인식 시작할 수 있습니다.

![4 결과 분석 및 음악 추천](https://github.com/user-attachments/assets/8d51765f-1c44-4443-af64-eae4cb30a406)

---

#### 📱 모바일 환경

Moodify는 반응형 디자인을 채택하여 **모바일에서도 완벽히 작동**합니다.

**Responsinator**를 통해 테스트:  
- [Responsinator](http://www.responsinator.com/)에 접속합니다.  
- URL 입력창에 로컬 서버 주소(`http://127.0.0.1:5000`)를 입력 후 실행합니다.

---

1️⃣ **모바일 첫 화면**  
- **Start Emotion Detection** 버튼을 터치하면 카메라가 실행됩니다.

![5 모바일 첫 화면](https://github.com/user-attachments/assets/d27d1e8a-14f1-4f64-96c6-deb08ebfc5be)

2️⃣ **모바일 카메라**  
- 5초 동안 카메라를 응시하면 실시간으로 감지되는 감정과 신뢰도를 확인할 수 있습니다.

![6 모바일 카메라](https://github.com/user-attachments/assets/e8f4bcb4-8c21-4b1e-82a9-acdf85c32aa7)

3️⃣ **모바일 결과 - 그래프와 분석 정보**  
- 감지된 감정과 신뢰도를 그래프와 함께 볼 수 있습니다.
- 감지된 감정에 따라 배경색과 그래프 색상이 동기화됩니다. 
- 그래프를 터치하면 더 자세한 정보(신뢰도, 감지 빈도수)가 표시됩니다.

![7 모바일 결과](https://github.com/user-attachments/assets/bf9bb24e-9deb-435e-b37a-2da78c23c8b1)

4️⃣ **모바일 결과 - 추천 플레이리스트**  
- 감지된 감정을 기반으로 추천된 플레이리스트와 노래 재생 버튼이 표시됩니다.
-  Start Emotion Detection 누르면 처음부터 다시 감정 인식 시작할 수 있습니다.

![8 모바일 결과 2](https://github.com/user-attachments/assets/17b679f4-e7ff-42f1-9d3d-e9ce3e2088b2)

## 📚 참고 자료
- [FER2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)
- [Spotify Web Playback SDK Documentation](https://developer.spotify.com/documentation/web-playback-sdk)
- [Spotify Web API Authorization Guide](https://developer.spotify.com/documentation/web-api)
- [Responsinator for Mobile Testing](http://www.responsinator.com)

---

## 🏆 프로젝트 소감 및 아쉬운 점

### 🎉 프로젝트 소감
Moodify 프로젝트는 딥러닝 기반 감정 분석과 음악 추천 기능을 결합한 새로운 시도를 담은 프로젝트입니다.  
실시간으로 사용자 감정을 인식하고, 이를 바탕으로 음악을 추천하며 사용자의 기분을 음악으로 전환하는 색다른 경험을 제공했습니다.  

이 프로젝트를 통해 다음과 같은 성장을 경험할 수 있었습니다:
- 딥러닝 모델 설계 및 학습 과정을 경험하며 데이터 불균형 문제 해결과 하이퍼파라미터 튜닝의 중요성을 이해했습니다.
- Spotify API와 같은 외부 플랫폼과의 통합을 통해 실제 환경에서의 API 활용 경험을 쌓았습니다.
- 반응형 디자인을 도입하여 모바일과 데스크톱 환경에서 모두 작동하는 인터페이스를 설계했습니다.

Moodify는 단순한 기술 구현을 넘어 사용자 경험을 고려한 프로젝트였으며, 이를 통해 창의적 사고와 기술적 도전 과정을 즐길 수 있었습니다. 🎧

---

### 🛑 한계 및 개선점

1️⃣ Spotify API 프리미엄 계정 이슈
- Spotify Web Playback SDK는 프리미엄 계정에서만 동작.
- 프로젝트 초기에는 무료 계정을 사용해 테스트를 진행하고 플레이리스트 목록을 가져오는 것을 성공했지만, 재생 기능이 작동하지 않았습니다.
- 프리미엄 계정으로 다시 시도했으나, **OAuth 인증 과정에서 토큰 문제**가 발생하여 완전한 구현이 어려웠습니다.
- 이를 해결하기 위해 더 많은 테스트와 프리미엄 계정 활용 방안을 모색해야 합니다.

2️⃣ 채팅 기능 및 영화 추천 기능 미구현
- 사용자 간 감정 및 음악을 공유할 수 있는 **채팅 기능**을 추가하고자 했으나, 시간 부족과 기술적 한계로 구현하지 못했습니다.
- 감정 분석 결과를 바탕으로 적합한 영화를 추천하는 **영화 추천 기능**도 구상했으나, 프로젝트 범위와 시간 제약으로 제외했습니다..

3️⃣ 서버 배포 미완료
- 현재 프로젝트는 **로컬 환경**에서만 실행 가능합니다.
- AWS, Heroku 등 클라우드 플랫폼을 통해 서버를 배포하면 더 많은 사용자 피드백을 받을 수 있습니다.
- 서버 배포가 완료되면 실시간 감정 분석 및 음악 추천 기능의 실제 사용성을 더욱 검증할 수 있습니다.

4️⃣ 딥러닝 모델 성능 향상 필요
- FER2013 데이터셋의 클래스 불균형 문제로 일부 감정(특히 Disgust)의 예측 정확도가 낮았습니다.
- 더 크고 다양한 데이터셋 활용 및 모델 구조 개선으로 성능 향상을 도모해야 합니다.

5️⃣ 실시간 분석 최적화 부족
- 일부 환경에서는 웹캠 입력 처리 속도가 느려지는 문제가 있었습니다.
- 딥러닝 모델의 경량화 및 코드 최적화를 통해 분석 속도를 개선해야 합니다.

---

## 💡 향후 개선 방향
- **서버 배포**: 클라우드 서비스를 활용해 프로젝트를 배포하고, 사용자 피드백을 수집하며 기능을 개선할 수 있습니다.
- **멀티모달 감정 분석**: 얼굴 표정뿐만 아니라 음성 감정 분석을 결합하여 더 정확한 감정 분석 시스템 구현할 수 있습니다.
- **음악 외 추천 기능 추**: 영화, 책 등 다양한 콘텐츠 추천을 통해 감정 기반 경험을 확장할 수 있습니다.
- **실시간 성능 최적화**: 처리 속도를 높이기 위해 경량 모델 도입 및 코드 최적화 진행할 수 있습니다.

Moodify는 현재의 모습에서 멈추지 않고, 계속 발전시켜 더 나은 사용자 경험과 기능을 제공할 가능성을 가지고 있습니다.  
사용자의 감정을 이해하고 이를 음악과 콘텐츠로 연결하는 여정을 통해 더 많은 사람들에게 즐거움을 선사하고 싶습니다!

---

## 📜 라이선스

이 프로젝트는 [MIT 라이선스](https://opensource.org/licenses/MIT)를 따릅니다.  
자세한 내용은 `LICENSE` 파일을 참조하세요.

---
