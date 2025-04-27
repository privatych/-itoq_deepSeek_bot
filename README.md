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
- Docker для контейнеризации

---

## Быстрый старт

### Вариант 1: Запуск через Docker (рекомендуется)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/privatych/-itoq_deepSeek_bot.git
   cd -itoq_deepSeek_bot
   ```

2. Создайте файл `.env` по примеру ниже и заполните своими ключами:
   ```
   BOT_TOKEN=ваш_telegram_token
   ADMIN_ID=ваш_telegram_id
   ```

3. Соберите и запустите Docker-контейнер:
   ```bash
   docker build -t deepseek-bot .
   docker run --env-file .env --rm deepseek-bot
   ```

### Вариант 2: Запуск без Docker

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/privatych/-itoq_deepSeek_bot.git
   cd -itoq_deepSeek_bot
   ```

2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # для Linux/Mac
   # или
   .venv\Scripts\activate  # для Windows
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` по примеру ниже и заполните своими ключами:
   ```
   BOT_TOKEN=ваш_telegram_token
   ADMIN_ID=ваш_telegram_id
   ```

4. Запустите бота:
   ```bash
   python main.py
   ```

---

## Структура проекта

```
-itoq_deepSeek_bot/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── admin_router.py
├── config.py
├── keyboards.py
├── main.py
├── requirements.txt
├── services.py
└── states.py
```

---

## Лицензия
MIT 