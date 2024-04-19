from datetime import datetime

import g4f
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.leaving_answer import LeaveAnswer

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import insert_answer, get_question_by_id

router = Router()


@router.callback_query(F.data.startswith('answer_'))
async def leave_answer(callback: CallbackQuery):
    await callback.message.answer(
        text="🤔Хотите ли Вы написать ответ самостоятельно или с помощью Тима?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🙋‍️Самостоятельно",
                                                   callback_data=f"a_self_{callback.data.split('_')[1]}")],
                             [InlineKeyboardButton(text=f"🤖С помощью Тима",
                                                   callback_data=f"a_tim_{callback.data.split('_')[1]}")]])
    )


@router.callback_query(F.data.startswith('a_tim_'))
async def leave_answer(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id)
    await state.update_data(question_id=callback.data.split('_')[2])
    try:
        user_data = await state.get_data()
        question = get_question_by_id(user_data["question_id"])
        text = "Представь, что ты - тим-лид it-отдела машиностроительного производства." \
               " Тебе необходимо ответить на данный тебе вопрос от младшего сотрудника компании. " \
               " В ответе оставь только сгенерированный тобой ответ без лишних надписей, только текст." \
               " Твой ответ не должен превышать лимит в 1500 знаков." \
               " Вопрос к тебе: " + question[0][4]
        await state.update_data(text=text)
        messages = [{"role": "user", "content": text}]
        responce = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=messages
        )
        await state.update_data(cur_answer=responce)
        await callback.message.answer(
            text=f"🤖Тим предлагает Вам ответить так: \n"
                 f"{responce}\n"
                 f"❓Одобрить данный ответ?",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=f"✅Одобрить",
                                                       callback_data="ok_ai_ans")],
                                 [InlineKeyboardButton(text=f"🏠Отменить и перейти на главную",
                                                       callback_data="main")]])
        )
    except:
        await callback.message.answer(
            text=f"🤖Тим, к сожлению, устал, и пока не может ответить на твой запрос😔",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную",
                                                       callback_data="main")]])
        )


@router.callback_query(F.data.startswith('ok_ai_ans'))
async def leave_answer(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    insert_answer(question_id=user_data["question_id"], user_id=user_data['user_id'], onModeration=1,
                  date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                  answer_text=user_data['cur_answer'], answer_photo_id=0, answer_video_id=0,
                  answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                  answer_video_note_id=0, answer_rating=0, isAI=1, answer_votes=0)
    await callback.message.answer(
        text="✅Ваш ответ был отправлен на модерацию!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"На главную", callback_data="main")]])
    )
    await state.clear()


@router.callback_query(F.data.startswith('a_self_'))
async def leave_answer(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id)
    await state.update_data(question_id=callback.data.split('_')[2])
    await callback.message.answer(
        text="📲Напишите текст своего ответа, либо отправьте изображение, видео, аудио, документ,"
             " голосовое сообщение или видео сообщение",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(LeaveAnswer.answer)


@router.message(LeaveAnswer.answer)
async def leave_feedback(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text is not None:
        insert_answer(question_id=user_data["question_id"], user_id=user_data['user_id'], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text=message.text, answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=0, answer_rating=0, isAI=0, answer_votes=0)
    elif message.photo is not None:
        insert_answer(question_id=user_data["question_id"], user_id=user_data['user_id'], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=message.photo[-1].file_id, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=0, answer_rating=0, isAI=0, answer_votes=0)
    elif message.video is not None:
        insert_answer(question_id=user_data["question_id"], user_id=user_data['user_id'], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=message.video.file_id,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=0, answer_rating=0, isAI=0, answer_votes=0)
    elif message.audio is not None:
        insert_answer(question_id=user_data["question_id"], user_id=user_data['user_id'], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=message.audio.file_id, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=0, answer_rating=0, isAI=0, answer_votes=0)
    elif message.document is not None:
        insert_answer(question_id=user_data["question_id"], user_id=user_data['user_id'], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=message.document.file_id, answer_voice_id=0,
                      answer_video_note_id=0, answer_rating=0, isAI=0, answer_votes=0)
    elif message.voice is not None:
        insert_answer(question_id=user_data["question_id"], user_id=user_data['user_id'], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=message.voice.file_id,
                      answer_video_note_id=0, answer_rating=0, isAI=0, answer_votes=0)
    elif message.video_note is not None:
        insert_answer(question_id=user_data["question_id"], user_id=user_data['user_id'], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=message.video_note.file_id,
                      answer_rating=0, isAI=0, answer_votes=0)
    question = get_question_by_id(user_data["question_id"])
    await message.answer(
        text="✅Ваш ответ был отправлен на модерацию!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"На главную", callback_data="main")]])
    )
    await state.clear()


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        get_start_text(),
        reply_markup=start_kb()
    )
