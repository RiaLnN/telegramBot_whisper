from faster_whisper import WhisperModel

model = WhisperModel(
    model_size_or_path='base',
    device='cpu',
    compute_type='int8',
    cpu_threads=2
)

def transcribe_audio(file_path: str) -> str:
    segments, _ = model.transcribe(
        audio=file_path,
        beam_size=1,
        language='ru'
    )

    full_text = []
    for segment in segments:
        full_text.append(segment.text)

    result_text = "".join(full_text).strip()

    return result_text