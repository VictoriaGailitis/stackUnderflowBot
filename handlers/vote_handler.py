from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import get_question_by_id, insert_vote_question, insert_vote_answer, \
    get_answer_by_id, update_votes_question, update_votes_answer, update_user_rating, get_user_by_id

router = Router()


@router.callback_query(F.data.startswith("vote_"))
async def answer_all(callback: CallbackQuery):
    type = callback.data.split('_')[1]
    if type == 'q':
        question_id = callback.data.split('_')[2]
        question = get_question_by_id(question_id)
        try:
            insert_vote_question(callback.message.from_user.id, question_id)
            user = get_user_by_id(callback.from_user.id)
            update_user_rating(user[0][0], user[0][6] + 30)
            user2 = get_user_by_id(question[0][1])
            update_user_rating(user2[0][0], user2[0][6] + 30)
            question_votes = int(question[0][14]) + 1
            update_votes_question(int(question_id), question_votes)
            answer_text = "✅Ваш голос за вопрос был зарегистрирован!"
        except:
            answer_text = "❗Вы уже отдали голос за этот вопрос!"
    else:
        answer_id = callback.data.split('_')[2]
        answer = get_answer_by_id(answer_id)
        try:
            insert_vote_answer(callback.message.from_user.id, answer_id)
            user = get_user_by_id(callback.from_user.id)
            update_user_rating(user[0][0], user[0][6] + 30)
            user2 = get_user_by_id(answer[0][2])
            update_user_rating(user2[0][0], user2[0][6] + 30)
            answer_votes = answer[0][14] + 1
            update_votes_answer(int(answer_id), answer_votes)
            answer_text = "✅Ваш голос за ответ был зарегистрирован!"
        except:
            answer_text = "❗Вы уже отдали голос за этот ответ!"
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
