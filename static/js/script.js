const socket = io();

// 감정별 배경색
const emotionColors = {
    happy: "#ffeb3b",
    sad: "#2196f3",
    angry: "#f44336",
    disgust: "#9c27b0",
    scared: "#607d8b",
    surprised: "#ff9800",
    neutral: "#9e9e9e"
};

// 그래프 막대 색상 조정 (배경과 대비되도록 밝기/채도 변경)
const adjustedEmotionColors = {
    happy: "#ffcc00",
    sad: "#1565c0",
    angry: "#d32f2f",
    disgust: "#7b1fa2",
    scared: "#455a64",
    surprised: "#e65100",
    neutral: "#616161"
};

// 그래프 초기화 설정
const chartOptions = {
    responsive: false,
    plugins: {
        legend: { labels: { font: { size: 16 } } }
    },
    scales: {
        y: { beginAtZero: true, ticks: { font: { size: 14 } } },
        x: { ticks: { font: { size: 14 } } }
    }
};

// 신뢰도 그래프
const ctxConfidence = document.getElementById("confidence-chart").getContext("2d");
const confidenceChart = new Chart(ctxConfidence, {
    type: "bar",
    data: {
        labels: ["Angry", "Disgust", "Scared", "Happy", "Sad", "Surprised", "Neutral"],
        datasets: [{
            label: "Emotion Confidence (%)",
            data: [0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
                adjustedEmotionColors.angry,
                adjustedEmotionColors.disgust,
                adjustedEmotionColors.scared,
                adjustedEmotionColors.happy,
                adjustedEmotionColors.sad,
                adjustedEmotionColors.surprised,
                adjustedEmotionColors.neutral
            ],
            borderColor: ["#000", "#000", "#000", "#000", "#000", "#000", "#000"],
            borderWidth: 2
        }]
    },
    options: chartOptions
});

// 빈도수 그래프
const ctxFrequency = document.getElementById("frequency-chart").getContext("2d");
const frequencyChart = new Chart(ctxFrequency, {
    type: "bar",
    data: {
        labels: ["Angry", "Disgust", "Scared", "Happy", "Sad", "Surprised", "Neutral"],
        datasets: [{
            label: "Emotion Frequency",
            data: [0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
                adjustedEmotionColors.angry,
                adjustedEmotionColors.disgust,
                adjustedEmotionColors.scared,
                adjustedEmotionColors.happy,
                adjustedEmotionColors.sad,
                adjustedEmotionColors.surprised,
                adjustedEmotionColors.neutral
            ],
            borderColor: ["#000", "#000", "#000", "#000", "#000", "#000", "#000"],
            borderWidth: 2
        }]
    },
    options: chartOptions
});

let player; // Web Playback SDK의 Player 인스턴스

// Spotify Access Token 갱신 함수
async function refreshAccessToken() {
    try {
        const response = await fetch("http://localhost:8888/get-token?refresh_token=[YOUR_REFRESH_TOKEN]");
        const data = await response.json();
        if (data.access_token) {
            console.log('New Access Token:', data.access_token);
            return data.access_token;
        } else {
            console.error('Failed to refresh Access Token:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Error refreshing Access Token:', error);
        return null;
    }
}


// Spotify Web Playback SDK 초기화
async function initializeSpotifyPlayer() {
    const token = await refreshAccessToken();
    if (!token) {
        alert("Failed to initialize Spotify Player due to token error.");
        return;
    }

    player = new Spotify.Player({
        name: "Moodify Player",
        getOAuthToken: cb => cb(token),
        volume: 0.5
    });

    // SDK 이벤트 리스너 추가
    player.addListener("ready", ({ device_id }) => {
        console.log("Ready with Device ID", device_id);
        alert(`Spotify Player Ready: ${device_id}`);
    });

    player.addListener("not_ready", ({ device_id }) => {
        console.log("Device ID has gone offline", device_id);
    });

    player.addListener("initialization_error", ({ message }) => {
        console.error("Initialization Error:", message);
    });

    player.addListener("authentication_error", ({ message }) => {
        console.error("Authentication Error:", message);
    });

    player.addListener("account_error", ({ message }) => {
        console.error("Account Error:", message);
    });

    player.connect();

    document.getElementById("togglePlay").onclick = async function () {
        try {
            const state = await player.getCurrentState();
            if (!state) {
                alert("Spotify Player is not active. Please open Spotify and select this device.");
                return;
            }
            await player.togglePlay();
        } catch (error) {
            console.error("Error toggling playback:", error);
        }
    };
}

// 실시간 감정 업데이트
socket.on("emotion_update", (data) => {
    const liveEmotionDisplay = document.getElementById("live-emotion-display");
    liveEmotionDisplay.style.display = "block";
    liveEmotionDisplay.innerText = `Real-Time Detected Emotion: ${data.emotion}, Confidence: ${(data.confidence * 100).toFixed(2)}%`;

    if (emotionColors[data.emotion]) {
        document.body.style.backgroundColor = emotionColors[data.emotion];
    }

    const emotionIndex = confidenceChart.data.labels.indexOf(data.emotion.charAt(0).toUpperCase() + data.emotion.slice(1));
    if (emotionIndex >= 0) {
        confidenceChart.data.datasets[0].data[emotionIndex] = (data.confidence * 100).toFixed(2);
        confidenceChart.update();

        frequencyChart.data.datasets[0].data[emotionIndex]++;
        frequencyChart.update();
    }
});

// 최종 감정 결과 및 음악 추천
socket.on("final_emotion", async (data) => {
    const finalResultDisplay = document.getElementById("final-result");
    const playlistRecommendations = document.getElementById("playlist-recommendations");

    finalResultDisplay.style.display = "block";
    finalResultDisplay.innerHTML = `<strong>Final Detected Emotion:</strong> ${data.emotion}, Confidence: ${(data.confidence * 100).toFixed(2)}%`;

    try {
        const response = await fetch(`/recommend-music/${data.emotion}`);
        const musicData = await response.json();

        playlistRecommendations.style.display = "block"; // 감정 분석 완료 후 표시
        playlistRecommendations.innerHTML = `<h3>Recommended Songs for ${data.emotion}:</h3>`;

        if (musicData.tracks) {
            musicData.tracks.forEach(track => {
                playlistRecommendations.innerHTML += `<p>${track.name} - ${track.artist}</p>`;
            });
        } else {
            playlistRecommendations.innerHTML += `<p>No recommendations available.</p>`;
        }

        document.getElementById("togglePlay").style.display = "block"; // 재생 버튼 표시
    } catch (error) {
        console.error("Error fetching recommended music:", error);
    }
});

// 감정 분석 시작 시 음악 추천 박스를 숨김
function startDetection() {
    const liveEmotionDisplay = document.getElementById("live-emotion-display");
    const finalResultDisplay = document.getElementById("final-result");
    const playlistRecommendations = document.getElementById("playlist-recommendations");

    confidenceChart.data.datasets[0].data.fill(0);
    frequencyChart.data.datasets[0].data.fill(0);
    confidenceChart.update();
    frequencyChart.update();

    document.body.style.backgroundColor = "#f0f2f5";
    liveEmotionDisplay.style.display = "none";
    finalResultDisplay.style.display = "none";
    finalResultDisplay.innerHTML = "";
    playlistRecommendations.style.display = "none"; // 감정 분석 시작 시 숨김

    socket.emit("start_detection");
}

// 초기화 함수
(async () => {
    await initializeSpotifyPlayer(); // Spotify Web Playback SDK 초기화
})();
