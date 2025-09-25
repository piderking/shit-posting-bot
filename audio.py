import yt_dlp
import os
from config import *

def get_audio_path(id: str) -> str:
    return os.path.join(AUDIO_DIR, f"{id}.mp3")

def download_yt_audio(id: str) -> str:
    
    url = f"https://www.youtube.com/watch?v={id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        "outtmpl":  os.path.join(AUDIO_DIR, id),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # or 'wav', 'm4a'
            'preferredquality': '192',
            
        },],
        'postprocessor_args': ["-t", "90"],

    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        ydl.download([url])
    print(f"\nCompleted Audio Download for: \n{url}")
    return get_audio_path(id)

if __name__ == "__main__":
    print(download_yt_audio("txIw1M2Wk2k"))