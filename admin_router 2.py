from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from keyboards import create_inline_keyboard
from aiogram.fsm.context import FSMContext
from states import BroadcastState
from services import get_all_users, set_user_active_status, get_stat
from logging import log, ERROR
from config import ADMIN_ID

admin_router = Router()

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            text="Добро пожаловать в панель администратора. Выбери нужную функцию:",
            parse_mode="HTML",
            reply_markup=await create_inline_keyboard(
                ["🚀Отправить рассылку", "📊Получить статистику"],
                ["send_broadcast_message", "get_stat"]
            )
        )

@admin_router.callback_query(F.data == "admin_menu")
async def cmd_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.delete()

    if callback.from_user.id == ADMIN_ID:
        await callback.message.answer(
            text="Добро пожаловать в панель администратора. Выбери нужную функцию:",
            parse_mode="HTML",
            reply_markup=await create_inline_keyboard(
                ["🚀Отправить рассылку", "📊Получить статистику"],
                ["send_broadcast_message", "get_stat"]
            )
        )

@admin_router.callback_query(F.data == "get_stat")
async def send_stat_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    if callback.from_user.id == ADMIN_ID:
        stat_data = await get_stat()

        message_text = (
            f"Статистика бота:\n"
            f"Кол-во пользователей: <b>{stat_data.get('users_count')}</b>\n"
            f"Кол-во активных пользователей: <b>{stat_data.get('active_users_count')}</b>\n"
            f"Кол-во неактивных пользователей: <b>{stat_data.get('no_active_users_count')}</b>\n"
            f"Пользователей, которые воспользовались стартовым промокодом: <b>{stat_data.get('count_users_start_promotion')}</b>"
        )

        await callback.message.answer(
            text=message_text,
            parse_mode="HTML",
            reply_markup=await create_inline_keyboard(
                ["⬅️Назад"],
                ["admin_menu"]
            )
        )

@admin_router.callback_query(F.data == "send_broadcast_message")
async def send_broadcast_message_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    msg = await callback.message.answer(
        text="Пришли мне сообщение для рассылки.",
        parse_mode="HTML",
        reply_markup=await create_inline_keyboard(
            ["⬅️Назад"],
            ["admin_menu"]
        )
    )

    await state.set_state(BroadcastState.broadcast_message)
    await state.update_data(last_message_id=msg.message_id)

@admin_router.message(BroadcastState.broadcast_message)
async def send_broadcast_message_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    last_message_id = state_data.get("last_message_id")

    await message.bot.delete_message(message.chat.id, last_message_id)

    if message.text:
        text_data = message.text
    else:
        text_data = message.caption

    photo = message.photo[-1] if message.photo else None
    video = message.video if message.video else None

    await state.update_data(text_data=text_data, photo=photo, video=video)

    if photo:
        await message.answer_photo(
            photo=photo.file_id,
            caption=text_data,
            parse_mode="HTML",
            reply_markup=await create_inline_keyboard(
                ["🚀Отправить", "❌Отменить"],
                ["send_broadcast_confirm", "admin_menu"]
            )
        )
    elif video:
        await message.answer_video(
            video=video.file_id,
            caption=text_data,
            parse_mode="HTML",
            reply_markup=await create_inline_keyboard(
                ["🚀Отправить", "❌Отменить"],
                ["send_broadcast_confirm", "admin_menu"]
            )
        )
    else:
        await message.answer(
            text=text_data,
            parse_mode="HTML",
            reply_markup=await create_inline_keyboard(
                ["🚀Отправить", "❌Отменить"],
                ["send_broadcast_confirm", "admin_menu"]
            )
        )

    await state.set_state(BroadcastState.confirm_message)

@admin_router.callback_query(F.data == "send_broadcast_confirm", BroadcastState.confirm_message)
async def send_broadcast_confirm_message(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.delete()

        message_data = await state.get_data()
        text_data = message_data.get("text_data")
        photo = message_data.get("photo")
        video = message_data.get("video")

        users = await get_all_users()
        if not users:
            await callback.message.answer("❌ Нет пользователей для рассылки")
            await state.clear()
            return

        total_users = len(users)
        success_count = 0
        failed_count = 0

        # Отправляем сообщение о начале рассылки
        progress_msg = await callback.message.answer(
            f"🔄 Начало рассылки...\n"
            f"Всего пользователей: {total_users}\n"
            f"Успешно отправлено: 0\n"
            f"Не удалось отправить: 0"
        )

        for i, user in enumerate(users, 1):
            try:
                if photo:
                    await callback.bot.send_photo(
                        user[0], 
                        photo.file_id, 
                        caption=text_data, 
                        parse_mode="HTML"
                    )
                elif video:
                    await callback.bot.send_video(
                        user[0], 
                        video.file_id, 
                        caption=text_data, 
                        parse_mode="HTML"
                    )
                else:
                    await callback.bot.send_message(
                        user[0], 
                        text_data, 
                        parse_mode="HTML"
                    )
                success_count += 1
                await set_user_active_status(user[0], True)
            except Exception as e:
                failed_count += 1
                await set_user_active_status(user[0], False)
                log(level=ERROR, msg=f"Ошибка при отправке сообщения пользователю {user[0]}: {e}")

            # Обновляем сообщение о прогрессе каждые 10 пользователей
            if i % 10 == 0 or i == total_users:
                try:
                    await progress_msg.edit_text(
                        f"🔄 Рассылка в процессе...\n"
                        f"Всего пользователей: {total_users}\n"
                        f"Успешно отправлено: {success_count}\n"
                        f"Не удалось отправить: {failed_count}\n"
                        f"Прогресс: {i}/{total_users} ({int(i/total_users*100)}%)"
                    )
                except Exception as e:
                    log(level=ERROR, msg=f"Ошибка при обновлении сообщения о прогрессе: {e}")

        # Отправляем финальное сообщение о результатах
        await progress_msg.edit_text(
            f"✅ Рассылка завершена!\n\n"
            f"📊 Результаты:\n"
            f"• Всего пользователей: {total_users}\n"
            f"• Успешно отправлено: {success_count}\n"
            f"• Не удалось отправить: {failed_count}\n\n"
            f"Чтобы вернуться в меню, нажмите кнопку ниже",
            reply_markup=await create_inline_keyboard(
                ["⬅️Вернуться в меню"],
                ["admin_menu"]
            )
        )

        await state.clear()

    except Exception as e:
        log(level=ERROR, msg=f"Критическая ошибка при рассылке: {e}")
        await callback.message.answer(
            f"❌ Произошла критическая ошибка при рассылке: {str(e)}\n"
            "Пожалуйста, попробуйте позже или обратитесь к разработчику."
        )
        await state.clear() 