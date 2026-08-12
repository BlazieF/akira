import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from config.settings import MEM_USERS, MEM_CHANNELS, MEM_GLOBAL, MEM_SELF, MAX_MEMORY_LENGTH


class MemoryManager:
    """Управление памятью бота"""
    
    def __init__(self):
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """Создаёт директории для памяти"""
        os.makedirs(MEM_USERS, exist_ok=True)
        os.makedirs(MEM_CHANNELS, exist_ok=True)
        os.makedirs(os.path.dirname(MEM_GLOBAL), exist_ok=True)
    
    def get_user_memory(self, user_id: int) -> str:
        """Получает память о пользователе"""
        path = os.path.join(MEM_USERS, f"{user_id}.txt")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def save_user_memory(self, user_id: int, memory: str):
        """Сохраняет память о пользователе"""
        path = os.path.join(MEM_USERS, f"{user_id}.txt")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(memory[:MAX_MEMORY_LENGTH])  # лимит памяти
    
    def get_channel_history(self, channel_id: int) -> List[Dict]:
        """Получает историю канала"""
        path = os.path.join(MEM_CHANNELS, f"{channel_id}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # Повреждённый/пустой файл истории — начинаем с чистого листа
                    return []
        return []
    
    def save_channel_history(self, channel_id: int, history: List[Dict]):
        """Сохраняет историю канала"""
        path = os.path.join(MEM_CHANNELS, f"{channel_id}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(history[-20:], f, ensure_ascii=False, indent=2)  # храним последние 20
    
    def get_self_memory(self) -> str:
        """Получает память бота о себе"""
        if os.path.exists(MEM_SELF):
            with open(MEM_SELF, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def update_user_summary(self, user_id: int, username: str, interaction_summary: str):
        """Обновляет краткую запись о взаимодействии"""
        current = self.get_user_memory(user_id)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        new_entry = f"\n[{timestamp}] {username}: {interaction_summary}"
        updated = (current + new_entry)[-MAX_MEMORY_LENGTH:]
        
        self.save_user_memory(user_id, updated)