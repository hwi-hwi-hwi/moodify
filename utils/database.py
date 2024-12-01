import sqlite3

def init_db():
    conn = sqlite3.connect('moodify.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            emotion TEXT,
            music_recommendations TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_emotion_data(emotion, music_list):
    conn = sqlite3.connect('moodify.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO emotion_data (emotion, music_recommendations)
        VALUES (?, ?)
    ''', (emotion, ', '.join(music_list)))
    conn.commit()
    conn.close()
