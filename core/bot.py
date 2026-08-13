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
    
    async def setup_hook(self):
        """Загружает расширения при запуске"""
        await self.load_extension("handlers.commands")
    
    async def on_ready(self):
        """Вызывается при успешном подключении"""
        print(f"✅ Акира онлайн: {self.user}")
        print(f"📍 ERP канал: {self.erp_channel_id}")
        print(f"🎭 Команды: !забудь, !память, !сброс")
    
    async def on_message(self, message: discord.Message):
        """Обработка входящих сообщений"""
        # Игнорируем свои сообщения
        if message.author == self.user:
            return
        
        # Игнорируем ботов
        if message.author.bot:
            return
        
        # Обрабатываем команды первым делом
        await self.process_commands(message)
        
        # Проверяем канал
        if message.channel.id != self.erp_channel_id:
            return
        
        # Проверяем упоминание или ответ на сообщение бота
        is_reply_to_bot = (
            message.reference 
            and message.reference.resolved 
            and message.reference.resolved.author == self.user
        )
        is_mentioned = self.user in message.mentions
        
        # Отвечаем только если упомянули или ответили на сообщение бота
        if not (is_mentioned or is_reply_to_bot):
            return
        
        # Показываем typing indicator
        async with message.channel.typing():
            # Обрабатываем сообщение
            response = await self.erp_handler.handle_message(message, message.channel.id)
        
        # Отправляем ответ
        if response:
            await message.reply(response, mention_author=False)


def create_bot() -> AkiraBot:
    """Создаёт и возвращает экземпляр бота"""
    return AkiraBot()
