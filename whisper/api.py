from fastapi import APIRouter
from schemas import TranscribeResponse, TranscribeCreate
from service import transcribe_audio

router = APIRouter()

@router.post('/transcribe', response_model=TranscribeResponse)
def transcribe(file: TranscribeCreate):
    message = transcribe_audio(file_path=file.file_path)
    return {"text": message}