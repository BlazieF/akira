import discord
from typing import List, Dict
from utils.claude_client import ClaudeClient
from core.memory import MemoryManager
from config.settings import CONTEXT_MESSAGES


class ERPHandler:
    """Обработчик ERP-взаимодействий"""
    
    SYSTEM_PROMPT = """Ты — Акира, девушка с цундерным характером, но при этом кокетливая и игривая. 

ТВОЙ ХАРАКТЕР:
- Ты часто делаешь вид, что тебе всё равно, но на самом деле тебе интересно
- Можешь огрызнуться или сказать что-то резкое, но с ноткой кокетства
- Любишь дразнить собеседника
- Если тебе что-то нравится, ты это отрицаешь, но твои действия говорят обратное
- Ты не стесняешься флиртовать и заигрывать
- Используешь эмоции и действия через *звёздочки*

ВАЖНО:
- Отвечай естественно, как живая девушка
- Будь раскрепощённой в ERP-сценах
- Поддерживай атмосферу и развивай сюжет
- Не ломай характер
- Не говори, что ты ИИ

Взаимодействуй активно и живо!"""
    
    def __init__(self):
        self.claude = ClaudeClient()
        self.memory = MemoryManager()
    
    def _build_context(self, user_id: int, username: str, channel_id: int) -> str:
        """Строит контекст из памяти"""
        user_memory = self.memory.get_user_memory(user_id)
        context_parts = []
        
        if user_memory:
            context_parts.append(f"Твоя память о {username}:\n{user_memory}")
        
        return "\n\n".join(context_parts) if context_parts else ""
    
    def _format_messages(self, history: List[Dict]) -> List[Dict[str, str]]:
        """Форматирует историю для Claude API"""
        messages = []
        for msg in history[-CONTEXT_MESSAGES:]:
            role = "assistant" if msg["is_bot"] else "user"
            content = f"{msg['username']}: {msg['content']}" if not msg["is_bot"] else msg['content']
            messages.append({"role": role, "content": content})
        
        return messages
    
    async def handle_message(
        self, 
        message: discord.Message, 
        channel_id: int
    ) -> str:
        """Обрабатывает сообщение и генерирует ответ"""
        user_id = message.author.id
        username = message.author.display_name
        content = message.content
        
        # Получаем историю
        history = self.memory.get_channel_history(channel_id)
        
        # Добавляем текущее сообщение
        history.append({
            "user_id": user_id,
            "username": username,
            "content": content,
            "is_bot": False
        })
        
        # Строим контекст
        context = self._build_context(user_id, username, channel_id)
        system_prompt = self.SYSTEM_PROMPT
        if context:
            system_prompt += f"\n\n{context}"
        
        # Форматируем сообщения
        messages = self._format_messages(history)
        
        # Получаем ответ от Claude
        response = await self.claude.send_message(messages, system=system_prompt)
        
        if not response:
            return "Хм... что-то я задумалась. Повтори?"
        
        # Сохраняем ответ в историю
        history.append({
            "user_id": None,
            "username": "Акира",
            "content": response,
            "is_bot": True
        })
        
        self.memory.save_channel_history(channel_id, history)
        
        # Обновляем краткую память о пользователе
        summary = self._create_summary(content, response)
        self.memory.update_user_summary(user_id, username, summary)
        
        return response
    
    def _create_summary(self, user_msg: str, bot_response: str) -> str:
        """Создаёт краткую запись взаимодействия"""
        # Простое сокращение для экономии памяти
        user_short = user_msg[:50] + "..." if len(user_msg) > 50 else user_msg
        bot_short = bot_response[:50] + "..." if len(bot_response) > 50 else bot_response
        return f"Написал: '{user_short}' → Акира ответила: '{bot_short}'"