import tempfile
from pathlib import Path

def get_destination_path(file_id: str) -> str:
    temp_dir = tempfile.gettempdir()
    voices_dir = Path(temp_dir) / "voices"
    voices_dir.mkdir(parents=True, exist_ok=True)
    return str(voices_dir / f"{file_id}.ogg")

def get_payload_for_ai(system_prompt: str, user_text: str):
    return {
        "messages": [
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': user_text
            }
        ],
        "model": "meta-llama/Llama-3.1-8B-Instruct:novita"
    }

def get_header_for_ai(api_key: str):
    return {
        "Authorization": f"Bearer {api_key}"
    }