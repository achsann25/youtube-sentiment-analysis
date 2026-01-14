import pandas as pd
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# 1. Load API Key dari file .env (Rahasia)
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

# --- KONFIGURASI ---
VIDEO_ID = '0BRFlBVWH3c'  # Ganti dengan ID Video Targetmu

def get_comments(api_key, video_id, max_results=10):
    if not api_key:
        print("❌ Error: API Key tidak ditemukan. Cek file .env kamu!")
        return None

    # Membangun layanan YouTube API
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Request data komentar
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            order="relevance"
        )
        response = request.execute()
        
        comments_data = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            text = comment['textDisplay']
            author = comment['authorDisplayName']
            like_count = comment['likeCount']
            comments_data.append([author, text, like_count])

        df = pd.DataFrame(comments_data, columns=['Username', 'Komentar', 'Likes'])
        return df

    except Exception as e:
        print(f"Error dari YouTube: {e}")
        return None

# --- EKSEKUSI ---
print("Sedang mengambil data...")
df_hasil = get_comments(API_KEY, VIDEO_ID)

if df_hasil is not None:
    print("\n✅ BERHASIL! Ini 5 Komentar Teratas:")
    print(df_hasil.head(5))
    df_hasil.to_csv('data_mentah.csv', index=False)