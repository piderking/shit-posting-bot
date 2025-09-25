import os
import yt_dlp  # type: ignore
import subprocess
from audio import get_audio_path
from video import get_video_path

from config import OUTPUT_DIR

def get_final(video_id: str, audio_id: str) -> str:
        return os.path.join(OUTPUT_DIR, f"{video_id}+{audio_id}.mp4")

def combine_audio(video_id: str, audio_id: str) -> str:
    video_path = get_video_path(video_id)
    audio_path = get_audio_path(audio_id)
    output_path = get_final(video_id, audio_id)
    if not os.path.exists(output_path):
        
        cmd = [
            'ffmpeg', '-y',
            '-stream_loop', '-1',  # loop video infinitely
            '-i', video_path,
            '-stream_loop', '-1',  # loop audio infinitely
            '-i', audio_path,
            '-filter_complex', '[1:a]volume=0.3[aud]',  # reduce audio volume
            '-map', '0:v',           # map video
            '-map', '[aud]',         # map filtered audio
            '-c:v', 'libx264',       # re-encode video to allow trimming
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-t', '30',               # final output duration
            output_path
        ]
        subprocess.run(cmd, check=True)
    return output_path

if __name__ == "__main__":
    print(combine_audio("5trjourUruc", "txIw1M2Wk2k"))