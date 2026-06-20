import os

def get_destination_path(file_id: str):
    base_dir = "/voices"
    
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
        
    return f"{base_dir}/{file_id}.ogg"

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