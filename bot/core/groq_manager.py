import time
import logging
from collections import deque
from threading import Lock
from typing import Optional
from bot.core.config import settings

logger = logging.getLogger(__name__)

class GroqKeyManager:
    def __init__(self, keys_string: str, ban_duration: int = 60):
        raw_keys = [k.strip() for k in keys_string.split(",") if k.strip()]
        
        if not raw_keys:
            raise ValueError("Список API ключей Groq пуст! Проверь .env файл.")

        self._active_keys = deque(raw_keys)
        self._banned_keys = {}
        self._ban_duration = ban_duration
        self._lock = Lock()

    def _refresh_banned_keys(self):
        now = time.time()
        released_keys = []
        
        for key, unban_time in list(self._banned_keys.items()):
            if now >= unban_time:
                released_keys.append(key)
                del self._banned_keys[key]
                
        if released_keys:
            self._active_keys.extend(released_keys)
            logger.info(f"Срок бана истек. Восстановлено ключей: {len(released_keys)}")

    def get_key(self) -> Optional[str]:
        with self._lock:
            self._refresh_banned_keys()

            if not self._active_keys:
                logger.error("Все API ключи Groq заблокированы по Rate Limit!")
                return None

            current_key = self._active_keys[0]
            self._active_keys.rotate(-1) 
            return current_key

    def ban_key(self, key: str):
        with self._lock:
            if key in self._active_keys:
                self._active_keys.remove(key)
                
            self._banned_keys[key] = time.time() + self._ban_duration
            logger.warning(f"Ключ ...{key[-6:]} забанен на {self._ban_duration}с из-за Rate Limit.")


groq_key_manager = GroqKeyManager(keys_string=settings.GROQ_KEYS, ban_duration=60)