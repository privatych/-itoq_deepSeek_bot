import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID администратора
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# API ключ DeepSeek
DEEPSEEK_API_KEY = "sk-d6405192902340c5a3c3b6275c8b4aae"

CHANNEL_USERNAME = "itoq_ai"  # Имя канала без @ 