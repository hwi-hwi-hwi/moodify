from flask import Flask, request, jsonify
from components.face_detection import detect_emotion

app = Flask(__name__)

@app.route('/detect-emotion', methods=['POST'])
def detect_emotion_route():
    """
    업로드된 이미지에서 감정을 감지하여 반환하는 API 엔드포인트.
    """
    # 업로드된 이미지 가져오기
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image provided"}), 400

    # 감정 분석
    result = detect_emotion(image)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
