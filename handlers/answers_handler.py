from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.pagination_answers_keyboard import pagination_kb_answers
from keyboards.start_keyboard import start_kb

from texts.answer_text import get_answer_text, get_answer_caption
from texts.start_text import get_start_text

from db import get_answers_by_question_id

router = Router()


@router.callback_query(F.data.startswith("see_answers_"))
async def answer_all(callback: CallbackQuery):
    question_id = callback.data.split('_')[2]
    records = get_answers_by_question_id(question_id)
    answers_count = len(records)
    if answers_count == 0:
        await callback.message.answer(text="⚠️ Еще никто не ответил на данный вопрос",
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
            answer_kb = pagination_kb_answers(answers_count, 1, question_id, isMine)
            await callback.message.answer(text=answer_text,
                                          parse_mode="HTML",
                                          reply_markup=answer_kb
                                          )
        elif first_answer[6] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = pagination_kb_answers(answers_count, 1, question_id, isMine)
            await callback.message.answer_photo(photo=first_answer[6],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[7] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = pagination_kb_answers(answers_count, 1, question_id, isMine)
            await callback.message.answer_video(video=first_answer[7],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[8] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = pagination_kb_answers(answers_count, 1, question_id, isMine)
            await callback.message.answer_audio(audio=first_answer[8],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[9] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = pagination_kb_answers(answers_count, 1, question_id, isMine)
            await callback.message.answer_document(document=first_answer[9],
                                                   caption=answer_text,
                                                   parse_mode="HTML",
                                                   reply_markup=answer_kb)
        elif first_answer[10] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = pagination_kb_answers(answers_count, 1, question_id, isMine)
            await callback.message.answer_voice(voice=first_answer[10],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[11] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = pagination_kb_answers(answers_count, 1, question_id, isMine)
            await callback.message.answer_video_note(video_note=first_answer[11])
            await callback.message.answer(text=answer_text,
                                          reply_markup=answer_kb)


@router.callback_query(F.data.startswith('apage_'))
async def answer_next(callback: CallbackQuery):
    question_id = callback.data.split('_')[2]
    page = int(callback.data.split("_")[1])
    records = get_answers_by_question_id(question_id)
    next_answer = records[page - 1]
    isMine = 0
    if callback.from_user.id == next_answer[2]:
        isMine = 1
    answer_count = len(records)
    if next_answer[5] != "":
        answer_text = get_answer_text(next_answer)
        answer_kb = pagination_kb_answers(answer_count, page, question_id, isMine)
        await callback.message.answer(text=answer_text,
                                      parse_mode="HTML",
                                      reply_markup=answer_kb
                                      )
    elif next_answer[6] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = pagination_kb_answers(answer_count, page, question_id, isMine)
        await callback.message.answer_photo(photo=next_answer[6],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[7] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = pagination_kb_answers(answer_count, page, question_id, isMine)
        await callback.message.answer_video(video=next_answer[7],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[8] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = pagination_kb_answers(answer_count, page, question_id, isMine)
        await callback.message.answer_audio(audio=next_answer[8],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[9] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = pagination_kb_answers(answer_count, page, question_id, isMine)
        await callback.message.answer_document(document=next_answer[9],
                                               caption=answer_text,
                                               parse_mode="HTML",
                                               reply_markup=answer_kb)
    elif next_answer[10] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = pagination_kb_answers(answer_count, page, question_id, isMine)
        await callback.message.answer_voice(voice=next_answer[10],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[11] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = pagination_kb_answers(answer_count, page, question_id, isMine)
        await callback.message.answer_video_note(video_note=next_answer[11])
        await callback.message.answer(text=answer_text,
                                      reply_markup=answer_kb)


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )
