from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.editing_question import EditQuestion

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import update_question

router = Router()


@router.callback_query(F.data.startswith('edit_q_'))
async def edit_question(callback: CallbackQuery, state: FSMContext):
    question_id = callback.data.split('_')[2]
    await state.update_data(question_id=question_id)
    await state.update_data(user_id=callback.from_user.id)
    await callback.message.answer(
        text="📲Напишите обновленный текст своего вопроса, либо отправьте изображение, видео, аудио, документ,"
             " голосовое сообщение или видео сообщение",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(EditQuestion.question)


@router.message(EditQuestion.question)
async def edit_question(message: Message, state: FSMContext):
    if message.text is not None:
        await state.update_data(question=message.text)
        await state.update_data(type=1)
    elif message.photo is not None:
        await state.update_data(question=message.photo[-1].file_id)
        await state.update_data(type=2)
    elif message.video is not None:
        await state.update_data(question=message.video.file_id)
        await state.update_data(type=3)
    elif message.audio is not None:
        await state.update_data(question=message.audio.file_id)
        await state.update_data(type=4)
    elif message.document is not None:
        await state.update_data(question=message.document.file_id)
        await state.update_data(type=5)
    elif message.voice is not None:
        await state.update_data(question=message.voice.file_id)
        await state.update_data(type=6)
    elif message.video_note is not None:
        await state.update_data(question=message.video_note.file_id)
        await state.update_data(type=7)
    await message.answer(
        text="🏷️Введите обновленные теги своего вопроса в формате тег1 тег2 тег3 (через пробел)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(EditQuestion.tags)


@router.message(EditQuestion.tags)
async def edit_question(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    user_data = await state.get_data()
    if user_data["type"] == 1:
        update_question(question_id=user_data['question_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text=user_data['question'], question_photo_id=0, question_video_id=0,
                        question_audio_id=0, question_document_id=0, question_voice_id=0,
                        question_video_note_id=0, tags=user_data['tags'])
    elif user_data["type"] == 2:
        update_question(question_id=user_data['question_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=user_data["question"], question_video_id=0,
                        question_audio_id=0, question_document_id=0, question_voice_id=0,
                        question_video_note_id=0, tags=user_data['tags'])
    elif user_data["type"] == 3:
        update_question(question_id=user_data['question_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=user_data["question"],
                        question_audio_id=0, question_document_id=0, question_voice_id=0,
                        question_video_note_id=0, tags=user_data['tags'])
    elif user_data["type"] == 4:
        update_question(question_id=user_data['question_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=0,
                        question_audio_id=user_data["question"], question_document_id=0, question_voice_id=0,
                        question_video_note_id=0, tags=user_data['tags'])
    elif user_data["type"] == 5:
        update_question(question_id=user_data['question_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=0,
                        question_audio_id=0, question_document_id=user_data["question"], question_voice_id=0,
                        question_video_note_id=0, tags=user_data['tags'])
    elif user_data["type"] == 6:
        update_question(question_id=user_data['question_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=0,
                        question_audio_id=0, question_document_id=0, question_voice_id=user_data["question"],
                        question_video_note_id=0, tags=user_data['tags'])
    elif user_data["type"] == 7:
        update_question(question_id=user_data['question_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=0,
                        question_audio_id=0, question_document_id=0, question_voice_id=0,
                        question_video_note_id=user_data["question"], tags=user_data['tags'])
    await message.answer(
        text="✅Ваш вопрос был обновлен!",
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
