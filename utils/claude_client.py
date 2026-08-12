import aiohttp
import time
from typing import List, Dict, Optional
from config.settings import (
    CLAUDE_API_KEY, 
    CLAUDE_BASE, 
    CLAUDE_VERSION, 
    CLAUDE_MODEL,
    CLAUDE_MODELS_URL,
    SWITCH_ON_STATUSES,
    FALLBACK_MODELS_TTL
)


class ClaudeClient:
    """Клиент для работы с Claude API"""
    
    def __init__(self):
        self.api_key = CLAUDE_API_KEY
        self.base_url = CLAUDE_BASE
        self.model = CLAUDE_MODEL
        self.fallback_models = []
        self.last_fallback_check = 0
    
    async def _get_fallback_models(self) -> List[str]:
        """Получает список доступных моделей"""
        now = time.time()
        if self.fallback_models and (now - self.last_fallback_check) < FALLBACK_MODELS_TTL:
            return self.fallback_models
        
        try:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": CLAUDE_VERSION
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(CLAUDE_MODELS_URL, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        models = [m.get("id") for m in data.get("data", [])]
                        self.fallback_models = models
                        self.last_fallback_check = now
                        return models
        except Exception as e:
            print(f"Ошибка получения моделей: {e}")
        
        return []
    
    async def send_message(
        self, 
        messages: List[Dict[str, str]], 
        system: str = "",
        max_tokens: int = 2048
    ) -> Optional[str]:
        """Отправляет запрос к Claude API"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": CLAUDE_VERSION,
            "content-type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages
        }
        
        if system:
            payload["system"] = system
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("content", [{}])[0].get("text", "")
                    
                    # Фолбэк на другие модели
                    if resp.status in SWITCH_ON_STATUSES:
                        fallback = await self._get_fallback_models()
                        if fallback:
                            for model in fallback:
                                payload["model"] = model
                                async with session.post(self.base_url, headers=headers, json=payload) as retry_resp:
                                    if retry_resp.status == 200:
                                        data = await retry_resp.json()
                                        return data.get("content", [{}])[0].get("text", "")
                    
                    print(f"Claude API error: {resp.status} - {await resp.text()}")
                    return None
        
        except Exception as e:
            print(f"Ошибка запроса к Claude: {e}")
            return None