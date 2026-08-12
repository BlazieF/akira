"""
Ядро бота Акиры
Содержит основную логику бота и управление памятью
"""

from .bot import AkiraBot, create_bot
from .memory import MemoryManager

__all__ = [
    'AkiraBot',
    'create_bot',
    'MemoryManager'
]