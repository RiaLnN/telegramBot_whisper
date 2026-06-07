import os

def get_destination_path(file_id: str):
    if not os.path.exists('voices'):
        os.mkdir("voices")
    return f"voices/{file_id}.ogg"

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