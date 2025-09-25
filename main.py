from pydantic import BaseModel
from tinydb import Query
from generate import search_yt
from structs import Audio, FinalRepr, Video, YoutubeVideo, struct_from_id, video_into_audio, struct_from_dict, Final
from typing import List, Union, Optional
from fastapi import FastAPI, Query as FQuery
from db import db
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/video/yt/query")
async def video_query(query: str, download: Optional[bool], max_results:Optional[int],) -> List[YoutubeVideo]:
    videos =  search_yt(query, max_results=max_results or 3)
    
    if download:
        for idx, _ in enumerate(videos):
            temp = videos[idx]
            temp.download()
            videos[idx] = temp
            
    return videos

@app.get("/audio/yt/query")
async def audio_query(query: str, download: Optional[bool], max_results:Optional[int],) -> List[YoutubeVideo]:
    videos =  search_yt(query, max_results=max_results or 3)
    audios = []
    
    if download:
        for idx, _ in enumerate(videos):
            temp = video_into_audio(videos[idx])
            temp.download()
            
            audios.append(temp)
            
    return videos

  

@app.get("/download/{id}")
async def download_from_id(id: str) -> Union[Video, Audio]:
    value = db.search(Query().id == id)[0]
    d = struct_from_dict(value)
    if not d.downloaded:
        d.download()
    return d 


class UploadFinal(BaseModel):
    video_id: str
    audio_id: str
    ty: List[str] = ["insta"]
@app.post("/upload/")
async def upload(final: UploadFinal) -> bool:
    # ty: List[str] = ["insta"]
    f = Final(
        video=struct_from_id(final.video_id), # type: ignore 
        audio=struct_from_id(final.audio_id), # type: ignore
    )
    
    f.upload(final.ty)
    
    return True


    
    

@app.get('/content/{db_name}')
async def get_content(db_name: str):
    return db.search(Query().db == db_name )
