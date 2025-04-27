# DeepSeek 💎 ITOQ — Telegram-бот на aiogram + DeepSeek

## Описание

Многофункциональный Telegram-бот на Python с поддержкой DeepSeek.

### Возможности:
- 💬 Чат с DeepSeek (общение с ИИ)
- 📝 Помощь с текстом (редактирование, улучшение, исправление)
- 🔍 Анализ кода (поиск ошибок, оптимизация, объяснения)
- Удобное меню и поддержка команд `/start`, `/menu`, `/help`

### Технологии:
- Python 3.10+
- aiogram 3.x
- DeepSeek API
- FSM (Finite State Machine) для управления режимами
- Логирование, обработка ошибок

---

## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/yourbotrepo.git
   cd yourbotrepo
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` по примеру ниже и заполните своими ключами.
4. Запустите бота:
   ```bash
   python main.py
   ```

---

## Быстрый старт с Docker

1. Соберите Docker-образ:
   ```bash
   docker build -t chatgpt-itoq-bot .
   ```
2. Запустите контейнер:
   ```bash
   docker run --env-file .env --rm chatgpt-itoq-bot
   ```

---

## Пример .env
```
BOT_TOKEN=ваш_telegram_token
OPENAI_API_KEY=sk-...
ADMIN_ID=123456789
```

---

## Лицензия
MIT 