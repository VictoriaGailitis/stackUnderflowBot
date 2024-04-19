from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

from keyboards.my_pagination_keyboard import my_pagination_kb
from keyboards.start_keyboard import start_kb
from keyboards.my_answers_keyboard import my_pagination_kb_answers

from texts.answer_text import get_answer_text, get_answer_caption

from texts.question_text import get_question_text, get_question_caption
from texts.start_text import get_start_text

from db import get_my_questions, get_my_answers

router = Router()


@router.callback_query(F.data == "get_my_questions")
async def question_all(callback: CallbackQuery):
    records = get_my_questions(callback.from_user.id)
    question_count = len(records)
    if question_count == 0:
        await callback.message.answer(text="⚠️ Вы еще не задали ни одного вопроса, либо все Ваши вопросы ожидают "
                                           "модерации",
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
            answer_kb = my_pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer(text=answer_text,
                                          parse_mode="HTML",
                                          reply_markup=answer_kb
                                          )
        elif first_question[5] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = my_pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_photo(photo=first_question[5],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[6] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = my_pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_video(video=first_question[6],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[7] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = my_pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_audio(audio=first_question[7],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[8] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = my_pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_document(document=first_question[8],
                                                   caption=answer_text,
                                                   parse_mode="HTML",
                                                   reply_markup=answer_kb)
        elif first_question[9] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = my_pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_voice(voice=first_question[9],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[10] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = my_pagination_kb(question_count, 1, first_question[0], isMine)
            await callback.message.answer_video_note(video_note=first_question[10])
            await callback.message.answer(text=answer_text,
                                          reply_markup=answer_kb)


@router.callback_query(F.data.startswith('my_page_'))
async def page(callback: CallbackQuery):
    records = get_my_questions(callback.from_user.id)
    page = int(callback.data.split("_")[2])
    next_question = records[page - 1]
    isMine = 0
    if callback.from_user.id == next_question[1]:
        isMine = 1
    question_count = len(records)
    if next_question[4] != "":
        answer_text = get_question_text(next_question)
        answer_kb = my_pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer(text=answer_text,
                                      parse_mode="HTML",
                                      reply_markup=answer_kb
                                      )
    elif next_question[5] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = my_pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_photo(photo=next_question[5],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[6] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = my_pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_video(video=next_question[6],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[7] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = my_pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_audio(audio=next_question[7],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[8] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = my_pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_document(document=next_question[8],
                                               caption=answer_text,
                                               parse_mode="HTML",
                                               reply_markup=answer_kb)
    elif next_question[9] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = my_pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_voice(voice=next_question[9],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[10] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = my_pagination_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_video_note(video_note=next_question[10])
        await callback.message.answer(text=answer_text,
                                      reply_markup=answer_kb)


@router.callback_query(F.data == "get_my_answers")
async def answer_all(callback: CallbackQuery):
    records = get_my_answers(callback.from_user.id)
    answers_count = len(records)
    if answers_count == 0:
        await callback.message.answer(text="⚠️ У Вас еще нет ответов, либо все Ваши ответы находятся на модерации.",
                                      parse_mode="HTML",
                                      reply_markup=InlineKeyboardMarkup(
                                          inline_keyboard=[
                                              [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
                                      )
    else:
        first_answer = records[0]
        isMine = 0
        if callback.from_user.id == first_answer[2]:
            isMine = 1
        if first_answer[5] != "":
            answer_text = get_answer_text(first_answer)
            answer_kb = my_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer(text=answer_text,
                                          parse_mode="HTML",
                                          reply_markup=answer_kb
                                          )
        elif first_answer[6] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = my_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_photo(photo=first_answer[6],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[7] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = my_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_video(video=first_answer[7],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[8] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = my_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_audio(audio=first_answer[8],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[9] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = my_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_document(document=first_answer[9],
                                                   caption=answer_text,
                                                   parse_mode="HTML",
                                                   reply_markup=answer_kb)
        elif first_answer[10] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = my_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_voice(voice=first_answer[10],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[11] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = my_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_video_note(video_note=first_answer[11])
            await callback.message.answer(text=answer_text,
                                          reply_markup=answer_kb)


@router.callback_query(F.data.startswith('my_a_page_'))
async def answer_next(callback: CallbackQuery):
    page = int(callback.data.split("_")[3])
    records = get_my_answers(callback.from_user.id)
    next_answer = records[page - 1]
    isMine = 0
    if callback.from_user.id == next_answer[2]:
        isMine = 1
    answer_count = len(records)
    if next_answer[5] != "":
        answer_text = get_answer_text(next_answer)
        answer_kb = my_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer(text=answer_text,
                                      parse_mode="HTML",
                                      reply_markup=answer_kb
                                      )
    elif next_answer[6] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = my_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_photo(photo=next_answer[6],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[7] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = my_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_video(video=next_answer[7],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[8] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = my_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_audio(audio=next_answer[8],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[9] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = my_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_document(document=next_answer[9],
                                               caption=answer_text,
                                               parse_mode="HTML",
                                               reply_markup=answer_kb)
    elif next_answer[10] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = my_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_voice(voice=next_answer[10],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[11] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = my_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_video_note(video_note=next_answer[11])
        await callback.message.answer(text=answer_text,
                                      reply_markup=answer_kb)


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )
