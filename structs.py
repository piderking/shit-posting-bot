import os
from pydantic import BaseModel
from typing import List, Optional, Self, Union

from tinydb import Query
from exceptions import AudioFileNotFound, DownloadException, UploadException
from video import download_yt_video
from audio import download_yt_audio
from datetime import datetime
from instagrapi.types import Media
from db import db
from config import DEBUG, LOG_DIR, PROGRAM_ID
class Author(BaseModel):
    name: str
    url: str


class DownloadAble(BaseModel):
    db: str
    
    ty: str
    url: str
    id: str

    downloaded: bool = False
   
    def download(self) -> str:
        if self.db == "video":
            if self.ty == "yt":
                v =  download_yt_video(self.id)
                self.downloaded = True
                db.upsert(self.model_dump(), Query().id == self.id)

                return v
        elif self.db == "audio":
            if self.ty == "yt":
            
                v =  download_yt_audio(self.id)
                self.downloaded = True
                return v
        raise DownloadException(f"Provider Type: {self.ty} is not recognized... Try Again")
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        User = Query()
        
        db.upsert(self.model_dump(), User.id == self.id)
    

    
class Video(DownloadAble):
    db: str = "video"
    
    title: str
    description: Optional[str]
    duration: float
    
    thumbnails: Optional[List[str]]
    views: Optional[int]

    
class YoutubeVideo(Video):
    ty: str = "yt"

    
class Audio(DownloadAble):
    db: str = "audio"
    title: str
    description: Optional[str]
    duration: float
    views: Optional[int]


    
class YoutubeAudio(Audio):
    ty: str = "yt"


def struct_from_dict(data: dict) -> Union[Audio, Video]:
    kind = data.get("db")
    
    if kind == "video":
        return Video(**data)
    elif kind == "audio":
        return Audio(**data)
        
            
    
    raise Exception("unspecified kind")

def struct_from_id(id: str) -> Union[Audio, Video]:
    data = db.search(Query().id == id)[0]
    kind = data.get("db")
    
    if kind == "video":
        return Video(**data)
    elif kind == "audio":
        return Audio(**data)
        
            
    
    raise Exception("unspecified kind")

def video_into_audio(video: Video) -> Audio:    
    
    return  Audio(
            ty=video.ty,
            id=video.id,
            url=video.url,
            downloaded=video.downloaded,
            title=video.title,
            description=video.description,
            duration=video.duration,
            views=video.views,
        )

from output import combine_audio, get_final
from upload import login, make_thumbnail, upload_insta

from audio import get_audio_path
from video import get_video_path
from exceptions import AudioFileNotFound, VideoFileNotFound

class FinalRepr(BaseModel):
    video_id: str
    audio_id: str
    
    url: str
    final_path: str
class Final():
    # Where to upload it to
    audio: Audio
    video: Video
    final_path: Optional[str] = None
    def __init__(self, video: Video,  audio: Audio) -> None:
        self.video = video
        self.audio = audio
    
    def download(self) -> Self:
        self.audio.download()
        self.video.download()
        
        return self
    def build(self) -> Self:
        if not os.path.exists(get_video_path(self.video.id)):
            raise VideoFileNotFound(f"Video: {self.video.id} not found!")
        if not os.path.exists(get_audio_path(self.audio.id)):
            raise VideoFileNotFound(f"Audio: {self.audio.id} not found!")
        
        self.final_path = combine_audio(self.video.id, self.audio.id)
        
        return self
    
    def upload(self, ty: List[str]) -> List[Union[Media, None]]:
        # TODO Impletment for all types
        ret: List[Union[Media, None]] = [None for _ in ty]
        
        file = self.final_path or self.build().final_path
        
        # user stuff for instagram
        cl = login(os.getenv("INSTA_USER") or "ERROR", password=os.getenv("INSTA_PASSWORD"))

        for idx, tpy in enumerate(ty):
            if tpy == "insta":
                ret[idx] = upload_insta(cl, get_final(self.video.id, self.audio.id), title="Test Upload", thumbnail=make_thumbnail(self.video.id, self.audio.id))
                db.insert(FinalRepr(video_id=self.video.id, audio_id=self.audio.id, final_path=self.final_path or "", url=str(ret[idx].video_url) if ret[idx] is not None else "" ).model_dump()) # pyright: ignore[reportOptionalMemberAccess]

            else:
                raise UploadException(f"Couldn't find upload type: {tpy}")
        return ret
        

def get_log_file() -> str:
    return os.path.join(LOG_DIR, PROGRAM_ID+".log")


def export(f, item: str):
    content = f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]\n{item}\n"
    f.write(content)  # Write new text and a newline
    f.flush()  # Ensure data is written to disk immediately
    if DEBUG:
        print(item + '\n')
    
# Standalone log function
def log(*object) -> None:
    with open(get_log_file(), "a") as f:
        for obj in object:
            if type(obj) is str:
                export(f, obj)
            elif isinstance(obj, Video):
                # convert to
                video: Video = obj
                minutes, seconds = divmod(int(video.duration), 60)
                duration_str = f"{minutes}m {seconds}s"
                thumbs = "\n".join(video.thumbnails) if video.thumbnails else "No thumbnails"
                views_str = f"{video.views:,}" if video.views is not None else "Unknown"

                export(f, f"""
                    [Video Log]
                    Title      : {video.title}
                    Type       : {video.ty}
                    ID         : {video.id}
                    URL        : {video.url}
                    Description: {video.description or 'No description'}
                    Duration   : {duration_str}
                    Views      : {views_str}
                    Thumbnails :
                    {thumbs}
                """)
            
            else:
                export(f, str(obj))


