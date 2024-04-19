from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.pagination_tags_keyboard import pagination_tags_kb
from states.searching_tags import SearchTag

from keyboards.start_keyboard import start_kb
from texts.question_text import get_question_caption, get_question_text

from texts.start_text import get_start_text

from db import select_questions_by_tags

router = Router()


@router.callback_query(F.data == 'search_tags')
async def search_tag(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="🔍Введите один или несколько тегов для поиска в формате тег1 тег2 тег3",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SearchTag.tags)


@router.message(SearchTag.tags)
async def search_tag(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    user_data = await state.get_data()
    tags_array = user_data["tags"].split(" ")
    questions = select_questions_by_tags(tags_array)
    if len(questions) == 0:
        await message.answer(
            text="❌По данному(ым) тегу(ам) пока нет вопросов",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
        )
    else:
        first_question = questions[0]
        isMine = 0
        if message.from_user.id == first_question[1]:
            isMine = 1
        question_count = len(questions)
        if first_question[4] != "":
            answer_text = get_question_text(first_question)
            answer_kb = pagination_tags_kb(question_count, 1, first_question[0], isMine)
            await message.answer(text=answer_text,
                                          parse_mode="HTML",
                                          reply_markup=answer_kb
                                          )
        elif first_question[5] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_tags_kb(question_count, 1, first_question[0], isMine)
            await message.answer_photo(photo=first_question[5],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[6] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_tags_kb(question_count, 1, first_question[0], isMine)
            await message.answer_video(video=first_question[6],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[7] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_tags_kb(question_count, 1, first_question[0], isMine)
            await message.answer_audio(audio=first_question[7],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[8] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_tags_kb(question_count, 1, first_question[0], isMine)
            await message.answer_document(document=first_question[8],
                                                   caption=answer_text,
                                                   parse_mode="HTML",
                                                   reply_markup=answer_kb)
        elif first_question[9] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_tags_kb(question_count, 1, first_question[0], isMine)
            await message.answer_voice(voice=first_question[9],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[10] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = pagination_tags_kb(question_count, 1, first_question[0], isMine)
            await message.answer_video_note(video_note=first_question[10])
            await message.answer(text=answer_text,
                                          reply_markup=answer_kb)


@router.callback_query(F.data.startswith('tpage_'))
async def search_tag(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    tags_array = user_data["tags"].split(" ")
    records = select_questions_by_tags(tags_array)
    page = int(callback.data.split("_")[1])
    next_question = records[page - 1]
    isMine = 0
    if callback.from_user.id == next_question[1]:
        isMine = 1
    question_count = len(records)
    if next_question[4] != "":
        answer_text = get_question_text(next_question)
        answer_kb = pagination_tags_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer(text=answer_text,
                                    parse_mode="HTML",
                                    reply_markup=answer_kb
                                    )
    elif next_question[5] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_tags_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_photo(photo=next_question[5],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[6] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_tags_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_video(video=next_question[6],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[7] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_tags_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_audio(audio=next_question[7],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[8] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_tags_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_document(document=next_question[8],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[9] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_tags_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_voice(voice=next_question[9],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[10] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = pagination_tags_kb(question_count, page, next_question[0], isMine)
        await callback.message.answer_video_note(video_note=next_question[10])
        await callback.message.answer(text=answer_text,
                                    reply_markup=answer_kb)


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        get_start_text(),
        reply_markup=start_kb()
    )
