from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from keyboards import create_inline_keyboard
from aiogram.fsm.context import FSMContext
from states import UserStates
from services import add_user, get_user, set_user_active_status
from config import CHANNEL_USERNAME, ADMIN_ID, OPENAI_API_KEY
from logging import getLogger
import asyncio
from openai import AsyncOpenAI

logger = getLogger(__name__)
user_router = Router()

# Инициализация клиента OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def show_main_menu(message: Message):
    await message.answer(
        "🤖 Выберите нужную функцию:",
        reply_markup=await create_inline_keyboard(
            [
                "💬 Чат с ChatGPT",
                "🎨 Генерация изображений",
                "📝 Помощь с текстом",
                "🔍 Анализ кода",
                "ℹ️ Помощь"
            ],
            [
                "chat_gpt",
                "generate_image",
                "text_help",
                "code_analysis",
                "help"
            ]
        )
    )

@user_router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name

        # Добавляем пользователя в базу
        await add_user(user_id, username, first_name)

        # Показываем основное меню сразу, без проверки подписки
        await message.answer(
            f"👋 Привет, {first_name}!\n\n"
            "Добро пожаловать в ChatGPT бот! 🤖\n\n"
            "Я могу помочь тебе с:\n"
            "• 💬 Общением и ответами на вопросы\n"
            "• 🎨 Генерацией изображений\n"
            "• 📝 Анализом текста\n"
            "• 🔍 Анализом кода\n\n"
            "Выбери нужную функцию:",
            reply_markup=await create_inline_keyboard(
                ["💬 Чат с ChatGPT", "🎨 Генерация изображений", "📝 Текст", "🔍 Анализ кода", "ℹ️ Помощь"],
                ["chat_gpt", "generate_image", "text_help", "code_analysis", "help"]
            )
        )
        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка в обработке команды /start: {e}")
        await message.answer("Извините, произошла ошибка. Пожалуйста, попробуйте позже.")

@user_router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    try:
        await callback.answer()
        help_text = (
            "🤖 Я ChatGPT бот\n\n"
            "📝 Доступные функции:\n"
            "- 💬 Чат с ChatGPT - общение с ИИ\n"
            "- 🎨 Генерация изображений - создание картинок по описанию\n"
            "- 📝 Помощь с текстом - помощь в написании и редактировании\n"
            "- 🔍 Анализ кода - помощь с программированием\n\n"
            "🔍 Просто выберите нужную функцию в меню!"
        )
        await callback.message.answer(help_text)
        await show_main_menu(callback.message)
    except Exception as e:
        logger.error(f"Ошибка в обработке callback help: {e}")
        await callback.message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

@user_router.callback_query(F.data == "chat_gpt")
async def chat_gpt_callback(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.set_state(UserStates.waiting_for_prompt)
        await callback.message.answer(
            "💬 Отправьте ваш вопрос или сообщение для ChatGPT.\n"
            "Я постараюсь дать максимально полезный ответ!\n\n"
            "Чтобы вернуться в меню, отправьте команду /menu"
        )
    except Exception as e:
        logger.error(f"Ошибка в обработке chat_gpt: {e}")
        await callback.message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

@user_router.callback_query(F.data == "generate_image")
async def generate_image_callback(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.set_state(UserStates.waiting_for_image_prompt)
        logger.info(f"Пользователь {callback.from_user.id} начал генерацию изображения")
        await callback.message.answer(
            "🎨 Опишите изображение, которое хотите создать.\n"
            "Например: 'Кот в шляпе, сидящий на луне'\n\n"
            "Чтобы вернуться в меню, отправьте команду /menu"
        )
    except Exception as e:
        logger.error(f"Ошибка в обработке generate_image: {e}")
        await callback.message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

@user_router.callback_query(F.data == "text_help")
async def text_help_callback(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.set_state(UserStates.waiting_for_prompt)
        await callback.message.answer(
            "📝 Отправьте текст, с которым нужна помощь.\n"
            "Я могу:\n"
            "- Исправить ошибки\n"
            "- Улучшить стиль\n"
            "- Сделать текст более формальным/неформальным\n"
            "- И многое другое!\n\n"
            "Чтобы вернуться в меню, отправьте команду /menu"
        )
    except Exception as e:
        logger.error(f"Ошибка в обработке text_help: {e}")
        await callback.message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

@user_router.callback_query(F.data == "code_analysis")
async def code_analysis_callback(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.set_state(UserStates.waiting_for_prompt)
        await callback.message.answer(
            "🔍 Отправьте код, который нужно проанализировать.\n"
            "Я могу:\n"
            "- Найти ошибки\n"
            "- Оптимизировать код\n"
            "- Объяснить, как он работает\n"
            "- Предложить улучшения\n\n"
            "Чтобы вернуться в меню, отправьте команду /menu"
        )
    except Exception as e:
        logger.error(f"Ошибка в обработке code_analysis: {e}")
        await callback.message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

@user_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await show_main_menu(message)

@user_router.message(UserStates.waiting_for_prompt)
async def handle_prompt(message: Message, state: FSMContext):
    try:
        if message.text == "/menu":
            await state.clear()
            await show_main_menu(message)
            return

        if not message.text:
            await message.answer("Пожалуйста, отправьте текстовое сообщение.")
            return

        # Получаем ответ от ChatGPT
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Отправляем ответ пользователю
        await message.answer(response.choices[0].message.content)
        
        # Сбрасываем состояние и показываем меню
        await state.clear()
        await show_main_menu(message)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await message.answer(f"Извините, произошла ошибка: {str(e)}. Пожалуйста, попробуйте позже.")
        await state.clear()
        await show_main_menu(message)

@user_router.message(UserStates.waiting_for_image_prompt)
async def handle_image_prompt(message: Message, state: FSMContext):
    try:
        if message.text == "/menu":
            await state.clear()
            await show_main_menu(message)
            return

        if not message.text:
            await message.answer("Пожалуйста, отправьте текстовое описание изображения.")
            return

        logger.info(f"Пользователь {message.from_user.id} запросил изображение: {message.text}")
        
        # Отправляем сообщение о начале генерации
        processing_msg = await message.answer("🔄 Генерация изображения...")
        
        try:
            # Генерация изображения
            response = await client.images.generate(
                model="dall-e-3",
                prompt=message.text,
                n=1,
                size="1024x1024",
                quality="standard",
                style="vivid"
            )
            
            logger.info(f"Изображение сгенерировано для пользователя {message.from_user.id}")
            
            # Удаляем сообщение о генерации
            await processing_msg.delete()
            
            # Отправляем изображение
            image_url = response.data[0].url
            await message.answer_photo(
                photo=image_url,
                caption=f"🎨 Изображение по запросу: {message.text}"
            )
            
        except Exception as e:
            # Удаляем сообщение о генерации в случае ошибки
            await processing_msg.delete()
            raise e
            
        # Сбрасываем состояние и показываем меню
        await state.clear()
        await show_main_menu(message)
        
    except Exception as e:
        logger.error(f"Ошибка при генерации изображения: {e}")
        error_message = str(e)
        if "rate_limit_exceeded" in error_message.lower():
            await message.answer(
                "⚠️ Превышен лимит запросов к API. Пожалуйста, подождите немного и попробуйте снова."
            )
        elif "authentication" in error_message.lower():
            await message.answer(
                "⚠️ Ошибка аутентификации API. Пожалуйста, обратитесь к администратору."
            )
        else:
            await message.answer(
                f"⚠️ Произошла ошибка при генерации изображения: {error_message}\n"
                "Пожалуйста, попробуйте другой запрос или обратитесь к администратору."
            )
        await state.clear()
        await show_main_menu(message)

@user_router.message(Command("help"))
async def cmd_help(message: Message):
    try:
        help_text = (
            "🤖 Я ChatGPT бот\n\n"
            "📝 Доступные функции:\n"
            "- 💬 Чат с ChatGPT - общение с ИИ\n"
            "- 🎨 Генерация изображений - создание картинок по описанию\n"
            "- 📝 Помощь с текстом - помощь в написании и редактировании\n"
            "- 🔍 Анализ кода - помощь с программированием\n\n"
            "🔍 Просто выберите нужную функцию в меню!"
        )
        await message.answer(help_text)
        await show_main_menu(message)
    except Exception as e:
        logger.error(f"Ошибка в команде help: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

@user_router.message()
async def handle_message(message: Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        if current_state == UserStates.waiting_for_prompt.state:
            await handle_prompt(message, state)
        elif current_state == UserStates.waiting_for_image_prompt.state:
            await handle_image_prompt(message, state)
        else:
            # По умолчанию — чат с ChatGPT
            await state.set_state(UserStates.waiting_for_prompt)
            await handle_prompt(message, state)
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await message.answer("Извините, произошла ошибка. Пожалуйста, попробуйте позже.") 