import subprocess
from typing import Union
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.types import Media
import os

import requests
from video import get_video_path
from output import get_final

load_dotenv()
# Login
from config import *
def get_user(user: str) -> str:
    return os.path.join(INSTA_DIR, f"{user}.json")


def login(user: str, password: str | None = None) -> Client:
    cl = Client()
    cl.delay_range = [1, 3]

    # proxy = "http://miwihykr:kmod8mp6rxe8@142.111.48.253:7030"    # instead of hardcoding soax, use a random free proxy
    
    # print(f"Using proxy: {proxy}")
    # cl.set_proxy(proxy)

    if os.path.exists(get_user(user)):
        cl.load_settings(get_user(user))
        print("Loaded User from File")
    else:
        if password is None:
            raise Exception(
                f"If settings file doesn't exist, you must pass a password for user: {user}"
            )

        if cl.login(user, password):
            print("Successfully Logged In...")
            cl.dump_settings(get_user(user))
            print(f"Settings Written to {get_user(user)}")
        else:
            raise Exception(f"Error Logging into user: {user}")

    return cl


def get_thumbnail(video_id: str, audio_id: str) -> str:
    return os.path.join(IMAGE_DIR, f"{video_id}+{audio_id}.jpg")
def make_thumbnail(video_id: str, audio_id: str, timestamp: str = "00:00:05") -> str:
    """
    Extract a thumbnail from a video using ffmpeg.
    Args:
        video_path: input video file
        output_path: output image path (e.g., thumbnail.jpg)
        timestamp: when to take the frame (format: HH:MM:SS.xx)
    """
    cmd = [
        "ffmpeg",
        "-ss", timestamp,   # seek to timestamp
        "-i", get_video_path(video_id),   # input video
        "-frames:v", "1",   # extract 1 frame
        "-q:v", "2",        # quality (lower = better)
        os.path.join(IMAGE_DIR, f"{video_id}+{audio_id}.jpg")
    ]
    subprocess.run(cmd, check=True)
    
    return get_thumbnail(video_id, audio_id)

# TODO Generate Click Bait Captions
def upload_insta(cl: Client, file: str,  thumbnail: str, title: str="", description: str="", tags: list[str]=["funny"], ) -> Union[Media, None]:
    
    try:
        cl.video_upload(str(os.path.abspath(file)), caption=f"{title}\n{description}\n#{'#'.join(tags)}", thumbnail=thumbnail ) # type: ignore
    except Exception as e:
        print("Exception: " + str(e))
        return None
    finally:
        return None
    
if __name__ == "__main__":
    pat = get_final("5trjourUruc", "txIw1M2Wk2k")
    
    upload_insta(login(os.getenv("INSTA_USER") or "ERROR", password=os.getenv("INSTA_PASSWORD")), pat, thumbnail=make_thumbnail("5trjourUruc", "txIw1M2Wk2k"), title="Test Upload")