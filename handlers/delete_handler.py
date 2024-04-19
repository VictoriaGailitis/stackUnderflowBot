from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import not_moderate_answer, not_moderate_question

router = Router()


@router.callback_query(F.data.startswith("delete_q_"))
async def delete_question(callback: CallbackQuery):
    question_id = callback.data.split('_')[2]
    not_moderate_question(question_id)
    await callback.message.answer(text="✅Вопрос удален успешно!",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]]))

@router.callback_query(F.data.startswith("delete_a_"))
async def delete_answer(callback: CallbackQuery):
    answer_id = callback.data.split('_')[2]
    not_moderate_answer(answer_id)
    await callback.message.answer(text="✅Ответ удален успешно!",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]]))


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )
