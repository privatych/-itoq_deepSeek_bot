from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def create_inline_keyboard(buttons_text: list, buttons_data: list) -> InlineKeyboardMarkup:
    keyboard = []
    for text, data in zip(buttons_text, buttons_data):
        keyboard.append([InlineKeyboardButton(text=text, callback_data=data)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 