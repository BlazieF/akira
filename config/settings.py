import os
from pathlib import Path

# ====================== Пути ======================
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = "/app/data/economy.db"
MEM_DIR = "/app/data/memory"
MEM_GLOBAL = os.path.join(MEM_DIR, "akira.txt")
MEM_CHANNELS = os.path.join(MEM_DIR, "channels")
MEM_USERS = os.path.join(MEM_DIR, "users")
MEM_SELF = os.path.join(MEM_DIR, "self.txt")

# ====================== Discord ===================
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
ERP_CHANNEL_ID = 1537239216335880232
OWNER_ID = 1498061475535654942

# ====================== Claude API ================
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_BASE = "https://router.cheap/v1/messages"
CLAUDE_MODELS_URL = CLAUDE_BASE.rsplit("/messages", 1)[0] + "/models"
CLAUDE_VERSION = "2023-06-01"
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

SWITCH_ON_STATUSES = {404, 429, 503, 529, 403}
FALLBACK_MODELS_TTL = 300

# ====================== Лимиты ====================
MAX_MEMORY_LENGTH = 3000  # символов для краткой памяти
CONTEXT_MESSAGES = 15  # сообщений в контексте
