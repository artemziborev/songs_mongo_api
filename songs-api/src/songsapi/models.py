# FastAPI's jsonable_encoder handles converting various non-JSON types,
# such as datetime between JSON types and native Python types.
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import date

from .objectid import PydanticObjectId

class Song(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    artist: str
    title: str
    difficulty: float
    level:int
    released: date
    song_id:int
    rating: Optional[Dict]

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)