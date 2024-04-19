from datetime import datetime
import g4f
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.leaving_question import LeaveQuestion
from states.ai_question import AIQuestion

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import insert_question

router = Router()


@router.callback_query(F.data == 'leave_question')
async def leave_question(callback: CallbackQuery):
    await callback.message.answer(
        text="🤔Хотите ли Вы написать вопрос самостоятельно или с помощью Тима?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🙋‍️Самостоятельно", callback_data="question_self")],
                             [InlineKeyboardButton(text=f"🤖С помощью Тима", callback_data="question_tim")]])
    )


@router.callback_query(F.data == 'question_tim')
async def leave_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="📲Введите тему или вопрос, который необходимо раскрыть подробнее: ",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AIQuestion.theme)


@router.message(AIQuestion.theme)
async def leave_question(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    try:
        user_data = await state.get_data()
        text = "Представь, что ты - тим-лид it-отдела машиностроительного производства." \
               " Тебе необходимо придумать вопрос на заданную тему, либо же раскрыть данный тебе вопрос. " \
               " В ответе оставь только сгенерированный тобой вопрос без лишних надписей, только текст." \
               " Твой ответ не должен превышать лимит в 1500 знаков." \
               " Твоя тема или вопрос: " + user_data["theme"]
        await state.update_data(text=text)
        messages = [{"role": "user", "content": text}]
        responce = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=messages
        )
        await state.update_data(cur_question=responce)
        await message.answer(
            text=f"🤖Тим предлагает Вам задать такой вопрос: \n"
                 f"{responce}\n"
                 f"❓Одобрить данный вопрос?",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=f"✅Одобрить",
                                                       callback_data="ok_ai")],
                                 [InlineKeyboardButton(text=f"🏠Отменить и перейти на главную",
                                                       callback_data="main")]])
        )
    except:
        await message.answer(
            text=f"🤖Тим, к сожлению, устал, и пока не может ответить на твой запрос😔",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную",
                                                       callback_data="main")]])
        )


@router.callback_query(F.data == 'ok_ai')
async def leave_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="🏷️Введите теги своего вопроса в формате тег1 тег2 тег3 (через пробел)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AIQuestion.tags)


@router.message(AIQuestion.tags)
async def leave_question(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    user_data = await state.get_data()
    insert_question(user_id=message.from_user.id, onModeration=1,
                    date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                    question_text=user_data['cur_question'], question_photo_id=0, question_video_id=0,
                    question_audio_id=0, question_document_id=0, question_voice_id=0,
                    question_video_note_id=0, question_rating=0, isAI=1, tags=user_data['tags'], question_votes=0)
    await message.answer(
        text="✅Ваш вопрос был отправлен на модерацию!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
    )
    await state.clear()


@router.callback_query(F.data == 'question_self')
async def leave_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id)
    await callback.message.answer(
        text="📲Напишите текст своего вопроса, либо отправьте изображение, видео, аудио, документ,"
             " голосовое сообщение или видео сообщение",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(LeaveQuestion.question)


@router.message(LeaveQuestion.question)
async def leave_question(message: Message, state: FSMContext):
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
        text="🏷️Введите теги своего вопроса в формате тег1 тег2 тег3 (через пробел)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(LeaveQuestion.tags)


@router.message(LeaveQuestion.tags)
async def leave_question(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    user_data = await state.get_data()
    if user_data["type"] == 1:
        insert_question(user_id=user_data['user_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text=user_data['question'], question_photo_id=0, question_video_id=0,
                        question_audio_id=0, question_document_id=0, question_voice_id=0,
                        question_video_note_id=0, question_rating=0, isAI=0, tags=user_data['tags'], question_votes=0)
    elif user_data["type"] == 2:
        insert_question(user_id=user_data['user_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=user_data["question"], question_video_id=0,
                        question_audio_id=0, question_document_id=0, question_voice_id=0,
                        question_video_note_id=0, question_rating=0, isAI=0, tags=user_data['tags'], question_votes=0)
    elif user_data["type"] == 3:
        insert_question(user_id=user_data['user_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=user_data["question"],
                        question_audio_id=0, question_document_id=0, question_voice_id=0,
                        question_video_note_id=0, question_rating=0, isAI=0, tags=user_data['tags'], question_votes=0)
    elif user_data["type"] == 4:
        insert_question(user_id=user_data['user_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=0,
                        question_audio_id=user_data["question"], question_document_id=0, question_voice_id=0,
                        question_video_note_id=0, question_rating=0, isAI=0, tags=user_data['tags'], question_votes=0)
    elif user_data["type"] == 5:
        insert_question(user_id=user_data['user_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=0,
                        question_audio_id=0, question_document_id=user_data["question"], question_voice_id=0,
                        question_video_note_id=0, question_rating=0, isAI=0, tags=user_data['tags'], question_votes=0)
    elif user_data["type"] == 6:
        insert_question(user_id=user_data['user_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=0,
                        question_audio_id=0, question_document_id=0, question_voice_id=user_data["question"],
                        question_video_note_id=0, question_rating=0, isAI=0, tags=user_data['tags'], question_votes=0)
    elif user_data["type"] == 7:
        insert_question(user_id=user_data['user_id'], onModeration=1,
                        date_posted=datetime.now().strftime("%d.%m.%Y %H:%M"),
                        question_text="", question_photo_id=0, question_video_id=0,
                        question_audio_id=0, question_document_id=0, question_voice_id=0,
                        question_video_note_id=user_data["question"], question_rating=0, isAI=0,
                        tags=user_data['tags'], question_votes=0)

    await message.answer(
        text="✅Ваш вопрос был отправлен на модерацию!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
    )
    await state.clear()


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        get_start_text(),
        reply_markup=start_kb()
    )
