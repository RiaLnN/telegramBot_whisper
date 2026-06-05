from pydantic import BaseModel

class TranscribeCreate(BaseModel):
    file_path: str

class TranscribeResponse(BaseModel):
    text: str