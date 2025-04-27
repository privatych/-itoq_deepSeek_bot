from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from keyboards import create_inline_keyboard
from aiogram.fsm.context import FSMContext
from states import UserStates
from services import add_user, get_user, set_user_active_status
from config import CHANNEL_USERNAME, ADMIN_ID, DEEPSEEK_API_KEY
from logging import getLogger
import asyncio
import aiohttp

logger = getLogger(__name__)
user_router = Router()

async def get_deepseek_response(prompt: str) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_text = await response.text()
                raise Exception(f"API error: {error_text}")

async def show_main_menu(message: Message):
    await message.answer(
        "🤖 Выберите нужную функцию:",
        reply_markup=await create_inline_keyboard(
            [
                "💬 Чат с DeepSeek",
                "📝 Помощь с текстом",
                "🔍 Анализ кода",
                "ℹ️ Помощь"
            ],
            [
                "chat_gpt",
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
            "Добро пожаловать в DeepSeek бот! 🤖\n\n"
            "Я могу помочь тебе с:\n"
            "• 💬 Общением и ответами на вопросы\n"
            "• 📝 Анализом текста\n"
            "• 🔍 Анализом кода\n\n"
            "Выбери нужную функцию:",
            reply_markup=await create_inline_keyboard(
                ["💬 Чат с DeepSeek", "📝 Текст", "🔍 Анализ кода", "ℹ️ Помощь"],
                ["chat_gpt", "text_help", "code_analysis", "help"]
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
            "🤖 Я DeepSeek бот\n\n"
            "📝 Доступные функции:\n"
            "- 💬 Чат с DeepSeek - общение с ИИ\n"
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
            "💬 Отправьте ваш вопрос или сообщение для DeepSeek.\n"
            "Я постараюсь дать максимально полезный ответ!\n\n"
            "Чтобы вернуться в меню, отправьте команду /menu"
        )
    except Exception as e:
        logger.error(f"Ошибка в обработке chat_gpt: {e}")
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

        # Отправляем сообщение о начале обработки
        processing_msg = await message.answer("🔄 Обработка запроса...")
        
        try:
            # Получаем ответ от DeepSeek
            response = await get_deepseek_response(message.text)
            
            # Удаляем сообщение о обработке
            await processing_msg.delete()
            
            # Отправляем ответ пользователю
            await message.answer(response)
            
        except Exception as e:
            # Удаляем сообщение о обработке в случае ошибки
            await processing_msg.delete()
            raise e
            
        # Сбрасываем состояние и показываем меню
        await state.clear()
        await show_main_menu(message)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await message.answer(f"Извините, произошла ошибка: {str(e)}. Пожалуйста, попробуйте позже.")
        await state.clear()
        await show_main_menu(message)

@user_router.message()
async def handle_message(message: Message, state: FSMContext):
    try:
        # По умолчанию — чат с DeepSeek
        await state.set_state(UserStates.waiting_for_prompt)
        await handle_prompt(message, state)
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.") 