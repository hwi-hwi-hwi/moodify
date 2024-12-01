# 음악 추천 코드
def recommend_music(emotion):
    mock_music_data = {
        'happy': ['Song 1', 'Song 2'],
        'sad': ['Song 3', 'Song 4'],
        'neutral': ['Song 5', 'Song 6'],
        'angry': ['Song 7', 'Song 8'],
        'surprised': ['Song 9', 'Song 10']
    }
    return mock_music_data.get(emotion, [])
