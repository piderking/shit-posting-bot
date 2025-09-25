import os 
import uuid
from tinydb import TinyDB, Query

DATA_DIR = os.getenv("DATA_DIR") or "./data"
AUDIO_DIR = os.path.join(DATA_DIR, os.getenv("AUDIO_DIR") or "audio") 
VIDEO_DIR = os.path.join(DATA_DIR, os.getenv("VIDEO_DIR") or "video")
IMAGE_DIR = os.path.join(DATA_DIR, os.getenv("IMAGE_DIR") or "images")

OUTPUT_DIR = os.path.join(DATA_DIR, os.getenv("OUTPUT_DIR") or "output")
USER_DIR = os.path.join(DATA_DIR, os.getenv("USER_DIR") or "user")
INSTA_DIR = os.path.join(USER_DIR, os.getenv("INSTA_DIR") or "insta")
LOG_DIR = os.path.join(DATA_DIR, os.getenv("LOG_DIR") or "logs")

PROGRAM_ID = os.getenv("LOG_DIR") or str(uuid.uuid4())
DEBUG = bool(str(os.getenv("DEBUG")).lower()) or True
DB_DIR = os.path.join(DATA_DIR, os.getenv("DB_DIR") or "db")



dirs = [AUDIO_DIR, DATA_DIR, VIDEO_DIR, OUTPUT_DIR, USER_DIR, INSTA_DIR, LOG_DIR, DB_DIR, IMAGE_DIR]

for d in dirs:
    if not os.path.exists(d):
        print("Making Directory: " + d)
        os.makedirs(d)
        
print("All Directories Needed Exsist.")