from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import get_all_users, get_user_answers, get_user_questions

router = Router()


def sortUsers(val):
    return val[10]


@router.callback_query(F.data == "see_users")
async def authors_view(callback: CallbackQuery):
    users = get_all_users()
    users_new = []
    for user in users:
        user = list(user)
        user_answers = get_user_answers(user[1])
        user_questions = get_user_questions(user[1])
        user.append(len(user_answers))
        user.append(len(user_questions))
        users_new.append(user)
    users_new.sort(key=sortUsers, reverse=True)
    answer_text = "🧑🏻‍💻 Авторы вопросов и ответов:\n\n"
    for user in users_new:
        answer_text += f"👤{user[3]} {user[4] if user[4] is not None else ''}\n" \
                       f"💬Ответов: {user[10]}\n" \
                       f"❓Вопросов: {user[11]}\n" \
                       f"📲Контактные данные: @{user[2]}\n\n\n"
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
