import os
import yt_dlp  # type: ignore

from config import *

def get_video_path(id: str) -> str:
    return os.path.join(VIDEO_DIR, f"{id}.mp4")

def download_yt_video(id: str) -> str:
    url = f"https://www.youtube.com/watch?v={id}"

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(VIDEO_DIR, id),

        # ffmpeg filters: crop/scale video + lower audio volume
        'postprocessor_args': [
            '-vf', 'crop=in_h*9/16:in_h:(in_w-out_w)/2:0,scale=1080:1920',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-af', 'volume=0.3',   # 30% volume
            '-c:a', 'aac',
            '-b:a', '128k',
            '-t', '90'

        ],

        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }
        ]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
        ydl.download([url])

    print(f"\nCompleted Video Download for: \n{url}")

    return get_video_path(id)

if __name__ == "__main__":
    print(download_yt_video("5trjourUruc"))
