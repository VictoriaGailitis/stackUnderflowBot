from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import select_users_rating

router = Router()


@router.callback_query(F.data == "see_rating")
async def see_rating(callback: CallbackQuery):
    users = select_users_rating()
    answer_text = "🏆 Рейтинг наших пользователей: \n\n"
    for i in range(len(users)):
        answer_text += f"#{i+1} {users[i][3]} {users[i][4] if users[i][4] is not None else ''}\n" \
                       f"💻Аккаунт в тг: @{users[i][2]}\n" \
                       f"🥇Рейтинг: {users[i][6]}\n"
        if 0 <= users[i][6] <= 100:
            answer_text += "⭐Ранг: Новичок\n\n\n"
        elif 100 < users[i][6] <= 500:
            answer_text += "⭐Ранг: Рядовой\n\n\n"
        elif 500 < users[i][6] <= 1000:
            answer_text += "⭐Ранг: Опытный\n\n\n"
        elif 1000 < users[i][6] <= 5000:
            answer_text += "⭐Ранг: Гений\n\n\n"
        elif 5000 < users[i][6] <= 10000:
            answer_text += "⭐Ранг: Сверхразум\n\n\n"
        elif users[i][6] > 10000:
            answer_text += "⭐Ранг: Искусственный интеллект\n\n\n"

    await callback.message.answer(text=answer_text,
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]]))


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )
