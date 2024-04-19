from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

from keyboards.pagination_keyboard import pagination_kb
from keyboards.start_keyboard import start_kb
from handlers import leave_question_handler, leave_answer_handler, answers_handler, vote_handler, \
    search_tags_handler, edit_question_handler, edit_answer_handler, mailing_handler, authors_handler, \
    admin_handler, rating_handler, my_handler, delete_handler

from texts.question_text import get_question_text, get_question_caption
from texts.start_text import get_start_text

from db import get_all_questions, insert_user

router = Router()
router.include_routers(leave_question_handler.router, leave_answer_handler.router, answers_handler.router,
                       vote_handler.router, search_tags_handler.router, edit_question_handler.router,
                       edit_answer_handler.router, mailing_handler.router, authors_handler.router,
                       admin_handler.router, rating_handler.router, my_handler.router, delete_handler.router)


@router.message(Command("start"))
async def main_menu(message: Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    username = message.from_user.username
    insert_user(user_tg_id=user_id, username=username, user_first_name=user_first_name, user_last_name=user_last_name,
                isAdmin=0, user_rating=0, mail_answers=0, mail_tags="")
    await message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )


@router.callback_query(F.data == "see_all")
async def question_all(callback: CallbackQuery):
    records = get_all_questions()
    question_count = len(records)
    if question_count == 0:
        await callback.message.answer(text="⚠️ Еще никто не задал вопрос",
                                      parse_mode="HTML",
                                      reply_markup=InlineKeyboardMarkup(
                                          inline_keyboard=[
                                              [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
                                      )
    else:
        first_question = records[0]
        isMine = 0
        if callback.from_user.id == first_question[1]:
            isMine = 1
        if first_question[4] != "":
            answer_text = get_question_text(first_question)
            answer_kb = pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer(text=answer_text,
                                          parse_mode="HTML",
                                          reply_markup=answer_kb
                                          )
        elif first_question[5] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_photo(photo=first_question[5],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[6] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_video(video=first_question[6],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[7] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_audio(audio=first_question[7],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[8] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_document(document=first_question[8],
                                                   caption=answer_text,
                                                   parse_mode="HTML",
                                                   reply_markup=answer_kb)
        elif first_question[9] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_voice(voice=first_question[9],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[10] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_video_note(video_note=first_question[10])
            await callback.message.answer(text=answer_text,
                                          reply_markup=answer_kb)


@router.callback_query(F.data.startswith('page_'))
async def page(callback: CallbackQuery):
    records = get_all_questions()
    page = int(callback.data.split("_")[1])
    next_question = records[page - 1]
    isMine = 0
    if callback.from_user.id == next_question[1]:
        isMine = 1
    question_count = len(records)
    if next_question[4] != "":
        answer_text = get_question_text(next_question)
        answer_kb = pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer(text=answer_text,
                                      parse_mode="HTML",
                                      reply_markup=answer_kb
                                      )
    elif next_question[5] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_photo(photo=next_question[5],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[6] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_video(video=next_question[6],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[7] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_audio(audio=next_question[7],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[8] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_document(document=next_question[8],
                                               caption=answer_text,
                                               parse_mode="HTML",
                                               reply_markup=answer_kb)
    elif next_question[9] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_voice(voice=next_question[9],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[10] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_video_note(video_note=next_question[10])
        await callback.message.answer(text=answer_text,
                                      reply_markup=answer_kb)


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )
