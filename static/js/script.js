const socket = io();

// 감정별 배경색
const emotionColors = {
    happy: "#ffeb3b", // 기본 배경색
    sad: "#2196f3",
    angry: "#f44336",
    disgust: "#9c27b0",
    scared: "#607d8b",
    surprised: "#ff9800",
    neutral: "#9e9e9e"
};

// 그래프 막대 색상 조정 (배경과 대비되도록 밝기/채도 변경)
const adjustedEmotionColors = {
    happy: "#ffcc00", // 더 진한 노란색
    sad: "#1565c0",   // 더 어두운 파란색
    angry: "#d32f2f", // 더 어두운 빨간색
    disgust: "#7b1fa2", // 더 어두운 보라색
    scared: "#455a64", // 더 어두운 회색
    surprised: "#e65100", // 더 진한 주황색
    neutral: "#616161"   // 더 어두운 중립색
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
            borderColor: [
                "#000", "#000", "#000", "#000", "#000", "#000", "#000" // 모든 막대에 검은색 테두리 추가
            ],
            borderWidth: 2 // 테두리 두께
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
            borderColor: [
                "#000", "#000", "#000", "#000", "#000", "#000", "#000" // 모든 막대에 검은색 테두리 추가
            ],
            borderWidth: 2 // 테두리 두께
        }]
    },
    options: chartOptions
});

// 실시간 감정 업데이트
socket.on("emotion_update", (data) => {
    const liveEmotionDisplay = document.getElementById("live-emotion-display");
    liveEmotionDisplay.style.display = "block";
    liveEmotionDisplay.innerText = `Live Emotion: ${data.emotion}, Confidence: ${(data.confidence * 100).toFixed(2)}%`;

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

// 최종 감정 결과
socket.on("final_emotion", (data) => {
    const finalResultDisplay = document.getElementById("final-result");
    finalResultDisplay.style.display = "block";
    finalResultDisplay.innerHTML = `<strong>Final Emotion:</strong> ${data.emotion}, Confidence: ${(data.confidence * 100).toFixed(2)}%`;

    // 음악 추천 결과 표시
function fetchMusicRecommendations(emotion) {
    fetch(`/recommend-music/${emotion}`)
        .then(response => response.json())
        .then(data => {
            const finalResultDisplay = document.getElementById("final-result");
            finalResultDisplay.style.display = "block";

            if (data.error) {
                finalResultDisplay.innerHTML = `<strong>Error:</strong> ${data.error}`;
            } else {
                finalResultDisplay.innerHTML = `<strong>Recommended Songs for ${emotion}:</strong><br>`;
                data.tracks.forEach(track => {
                    finalResultDisplay.innerHTML += `${track.name} - ${track.artist}<br>`;
                });
            }
        });
}

// 감정 분석 결과 수신 시 음악 추천 요청
socket.on("final_emotion", (data) => {
    fetchMusicRecommendations(data.emotion);
});

});

// 감정 분석 시작
function startDetection() {
    const liveEmotionDisplay = document.getElementById("live-emotion-display");
    const finalResultDisplay = document.getElementById("final-result");

    confidenceChart.data.datasets[0].data.fill(0);
    frequencyChart.data.datasets[0].data.fill(0);
    confidenceChart.update();
    frequencyChart.update();

    document.body.style.backgroundColor = "#f0f2f5";
    liveEmotionDisplay.style.display = "none";
    finalResultDisplay.style.display = "none";
    finalResultDisplay.innerHTML = "";

    socket.emit("start_detection");
}
