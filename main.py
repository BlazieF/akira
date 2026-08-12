import os
from dotenv import load_dotenv

# Загружаем переменные окружения ДО импорта модулей,
# которые читают os.environ на уровне модуля (config.settings)
load_dotenv()

from core.bot import create_bot
from config.settings import DISCORD_TOKEN, CLAUDE_API_KEY


def main():
    """Точка входа"""
    # Проверяем наличие токенов
    if not DISCORD_TOKEN:
        raise ValueError("❌ DISCORD_TOKEN не найден в переменных окружения!")
    
    if not CLAUDE_API_KEY:
        raise ValueError("❌ CLAUDE_API_KEY не найден в переменных окружения!")
    
    # Создаём и запускаем бота
    bot = create_bot()
    
    print("🚀 Запуск Акиры...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()