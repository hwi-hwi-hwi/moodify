# 음악 추천 코드
def recommend_music(emotion):
    mock_music_data = {
        'Happy': ['Happy Song 1', 'Happy Song 2'],
        'Sad': ['Sad Song 1', 'Sad Song 2'],
        'Neutral': ['Neutral Song 1', 'Neutral Song 2'],
        'Angry': ['Angry Song 1', 'Angry Song 2'],
        'Surprising': ['Surprising Song 1', 'Surprising Song 2']
    }
    return mock_music_data.get(emotion, [])
