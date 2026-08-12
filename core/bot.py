import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN, ERP_CHANNEL_ID
from handlers.erp_handler import ERPHandler


class AkiraBot(commands.Bot):
    """Основной класс бота Акиры"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(command_prefix="!", intents=intents)
        
        self.erp_handler = ERPHandler()
        self.erp_channel_id = ERP_CHANNEL_ID
    
    async def on_ready(self):
        """Вызывается при успешном подключении"""
        print(f"✅ Акира онлайн: {self.user}")
        print(f"📍 ERP канал: {self.erp_channel_id}")
    
    async def on_message(self, message: discord.Message):
        """Обработка входящих сообщений"""
        # Игнорируем свои сообщения
        if message.author == self.user:
            return
        
        # Игнорируем ботов
        if message.author.bot:
            return
        
        # Проверяем канал
        if message.channel.id != self.erp_channel_id:
            return
        
        # Показываем typing indicator
        async with message.channel.typing():
            # Обрабатываем сообщение
            response = await self.erp_handler.handle_message(message, message.channel.id)
        
        # Отправляем ответ
        if response:
            await message.channel.send(response)
        
        # Обрабатываем команды (если есть)
        await self.process_commands(message)


def create_bot() -> AkiraBot:
    """Создаёт и возвращает экземпляр бота"""
    return AkiraBot()