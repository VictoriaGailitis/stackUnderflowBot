from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.editing_answer import EditAnswer

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import update_answer

router = Router()


@router.callback_query(F.data.startswith('edit_a_'))
async def leave_answer(callback: CallbackQuery, state: FSMContext):
    await state.update_data(answer_id=callback.data.split('_')[2])
    await callback.message.answer(
        text="📲Напишите обновленный текст своего ответа, либо отправьте изображение, видео, аудио, документ,"
             " голосовое сообщение или видео сообщение",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(EditAnswer.answer)


@router.message(EditAnswer.answer)
async def leave_feedback(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text is not None:
        update_answer(answer_id=user_data["answer_id"], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text=message.text, answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=0)
    elif message.photo is not None:
        update_answer(answer_id=user_data["answer_id"], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=message.photo[-1].file_id, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=0)
    elif message.video is not None:
        update_answer(answer_id=user_data["answer_id"], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=message.video.file_id,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=0)
    elif message.audio is not None:
        update_answer(answer_id=user_data["answer_id"], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=message.audio.file_id, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=0)
    elif message.document is not None:
        update_answer(answer_id=user_data["answer_id"], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=message.document.file_id, answer_voice_id=0,
                      answer_video_note_id=0)
    elif message.voice is not None:
        update_answer(answer_id=user_data["answer_id"], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=message.voice.file_id,
                      answer_video_note_id=0)
    elif message.video_note is not None:
        update_answer(answer_id=user_data["answer_id"], onModeration=1,
                      date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                      answer_text="", answer_photo_id=0, answer_video_id=0,
                      answer_audio_id=0, answer_document_id=0, answer_voice_id=0,
                      answer_video_note_id=message.video_note.file_id)
    await message.answer(
        text="✅Ваш ответ был обновлен!",
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