import os

def get_destination_path(file_id: str):
    if not os.path.exists('voices'):
        os.mkdir("voices")
    return f"voices/{file_id}.ogg"