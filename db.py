from typing import List, Dict
from pydantic import BaseModel
from config import DB_DIR
import os
from tinydb import TinyDB, Query

def to_db_path(db: str) -> str:
    return os.path.join(DB_DIR, db+".json")




db = TinyDB(to_db_path("db"))