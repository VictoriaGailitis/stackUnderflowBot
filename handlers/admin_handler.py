from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardRemove
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from keyboards.start_keyboard import start_kb
from keyboards.admin_questions_keyboard import admin_questions_pagination_kb
from keyboards.admin_answers_keyboard import admin_pagination_kb_answers

from texts.answer_text import get_answer_text, get_answer_caption
from texts.start_text import get_start_text
from texts.question_text import get_question_text, get_question_caption

from states.login_admin import LoginAdmin
from states.rating_question import RateQuestion
from states.rejecting_question import RejectQuestion
from states.rating_answer import RateAnswer
from states.rejecting_answer import RejectAnswer
from states.mailing_admin import MailAdmin

from handlers.schedule_handler import send_notification

from config_reader import config

from db import select_moderating_questions, get_question_by_id, moderate_question, not_moderate_question, \
    select_moderating_answers, get_answer_by_id, moderate_answer, not_moderate_answer, get_all_users,\
    get_last_question, insert_new_mailing, get_user_by_id, update_user_rating

from bot import bot

router = Router()


@router.callback_query(F.data == 'admin')
async def admin_log(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="📲Введите логин",
                                  reply_markup=ReplyKeyboardRemove())
    await state.set_state(LoginAdmin.login)


@router.message(LoginAdmin.login)
async def admin_log(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer(text="📲Введите пароль",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(LoginAdmin.password)


@router.message(LoginAdmin.password)
async def admin_log(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    user_data = await state.get_data()
    if user_data["login"] == config.admin_login.get_secret_value() and user_data[
        "password"] == config.admin_password.get_secret_value():
        answer_text = "⚙️Добро пожаловать в админ-панель!\n" \
                      "📝Здесь Вы можете одобрить или отклонить новые вопросы " \
                      "и ответы, а также оформить рассылку для всех пользователей данного бота.\n" \
                      "👉Выберите, с чего начать:"
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"❓Вопросы",
                                      callback_data="moderate_questions")],
                [InlineKeyboardButton(text=f"💬Ответы",
                                      callback_data="moderate_answers")],
                [InlineKeyboardButton(text=f"📩Создать рассылку",
                                      callback_data="admin_mailing")],
                [InlineKeyboardButton(text=f"🏠На главную",
                                      callback_data="main")]])
    else:
        answer_text = "❌ Неверный логин или пароль!"
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🏠На главную",
                                      callback_data="main")]])

    await message.answer(text=answer_text,
                         reply_markup=answer_kb)


@router.callback_query(F.data == 'moderate_questions')
async def moderate_questions(callback: CallbackQuery):
    questions = select_moderating_questions()
    if len(questions) == 0:
        answer_text = "⚠️Еще нет новых не отмодерированных вопросов"
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                      callback_data="main_admin")]])
        await callback.message.answer(text=answer_text,
                                      parse_mode="HTML",
                                      reply_markup=answer_kb
                                      )
    else:
        question_count = len(questions)
        first_question = questions[0]
        if first_question[4] != "":
            answer_text = get_question_text(first_question)
            answer_kb = admin_questions_pagination_kb(question_count, 1, first_question[0])
            await callback.message.answer(text=answer_text,
                                          parse_mode="HTML",
                                          reply_markup=answer_kb
                                          )
        elif first_question[5] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = admin_questions_pagination_kb(question_count, 1, first_question[0])
            await callback.message.answer_photo(photo=first_question[5],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[6] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = admin_questions_pagination_kb(question_count, 1, first_question[0])
            await callback.message.answer_video(video=first_question[6],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[7] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = admin_questions_pagination_kb(question_count, 1, first_question[0])
            await callback.message.answer_audio(audio=first_question[7],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[8] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = admin_questions_pagination_kb(question_count, 1, first_question[0])
            await callback.message.answer_document(document=first_question[8],
                                                   caption=answer_text,
                                                   parse_mode="HTML",
                                                   reply_markup=answer_kb)
        elif first_question[9] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = admin_questions_pagination_kb(question_count, 1, first_question[0])
            await callback.message.answer_voice(voice=first_question[9],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_question[10] != 0:
            answer_text = get_question_caption(first_question)
            answer_kb = admin_questions_pagination_kb(question_count, 1, first_question[0])
            await callback.message.answer_video_note(video_note=first_question[10])
            await callback.message.answer(text=answer_text,
                                          reply_markup=answer_kb)


@router.callback_query(F.data.startswith('mod_q_page_'))
async def moderate_questions_page(callback: CallbackQuery):
    records = select_moderating_questions()
    page = int(callback.data.split("_")[3])
    next_question = records[page - 1]
    question_count = len(records)
    if next_question[4] != "":
        answer_text = get_question_text(next_question)
        answer_kb = admin_questions_pagination_kb(question_count, page, next_question[0])
        await callback.message.answer(text=answer_text,
                                      parse_mode="HTML",
                                      reply_markup=answer_kb
                                      )
    elif next_question[5] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = admin_questions_pagination_kb(question_count, page, next_question[0])
        await callback.message.answer_photo(photo=next_question[5],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[6] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = admin_questions_pagination_kb(question_count, page, next_question[0])
        await callback.message.answer_video(video=next_question[6],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[7] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = admin_questions_pagination_kb(question_count, page, next_question[0])
        await callback.message.answer_audio(audio=next_question[7],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[8] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = admin_questions_pagination_kb(question_count, page, next_question[0])
        await callback.message.answer_document(document=next_question[8],
                                               caption=answer_text,
                                               parse_mode="HTML",
                                               reply_markup=answer_kb)
    elif next_question[9] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = admin_questions_pagination_kb(question_count, page, next_question[0])
        await callback.message.answer_voice(voice=next_question[9],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_question[10] != 0:
        answer_text = get_question_caption(next_question)
        answer_kb = admin_questions_pagination_kb(question_count, page, next_question[0])
        await callback.message.answer_video_note(video_note=next_question[10])
        await callback.message.answer(text=answer_text,
                                      reply_markup=answer_kb)


@router.callback_query(F.data.startswith('ok_q_'))
async def ok_moderate_questions_page(callback: CallbackQuery, state: FSMContext):
    question_id = int(callback.data.split("_")[2])
    await state.update_data(question_id=question_id)
    await callback.message.answer(text="⭐Оцените качество вопроса от 0 до 100",
                                  reply_markup=ReplyKeyboardRemove())
    await state.set_state(RateQuestion.rating)


@router.message(RateQuestion.rating)
async def admin_log(message: Message, state: FSMContext):
    await state.update_data(rating=message.text)
    user_data = await state.get_data()
    question_id = user_data["question_id"]
    question = get_question_by_id(question_id)
    rating = int(user_data["rating"])
    if question[0][12] == 0:  # если вопрос не создан с помошью ИИ
        rating += 100
    moderate_question(question_id, rating)
    users = get_all_users()
    for user in users:
        if user[8] != "" and user[8] is not None:
            for tag in user[8].split(" "):
                if tag in question[0][13].split(" "):
                    res = get_last_question()
                    insert_new_mailing(question[0][1], res[0][0])
    await bot.send_message(chat_id=question[0][1],
                           text=f"✅Ваш вопрос под номером {question_id} одобрен администратором!")
    user = get_user_by_id(question[0][1])
    new_rating = user[0][6] + rating + 50
    update_user_rating(user[0][0], new_rating)
    await message.answer(text="✅Вопрос одобрен успешно!",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                                       callback_data="main_admin")]]))


@router.callback_query(F.data.startswith('not_q_'))
async def not_moderate_questions_page(callback: CallbackQuery, state: FSMContext):
    question_id = int(callback.data.split("_")[2])
    await state.update_data(question_id=question_id)
    await callback.message.answer(text="✍️Напишите причину отказа в публикации",
                                  reply_markup=ReplyKeyboardRemove())
    await state.set_state(RejectQuestion.reason)


@router.message(RejectQuestion.reason)
async def admin_log(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    user_data = await state.get_data()
    question_id = user_data["question_id"]
    question = get_question_by_id(question_id)
    await bot.send_message(chat_id=question[0][1],
                           text=f"❌Ваш вопрос под номером {question_id} отклонен администратором!\n"
                                f"Причина: {user_data['reason']}")
    not_moderate_question(question_id)
    await message.answer(text="✅Вопрос отклонен успешно!",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                                       callback_data="main_admin")]]))


@router.callback_query(F.data == 'moderate_answers')
async def moderate_answers(callback: CallbackQuery):
    answers = select_moderating_answers()
    if len(answers) == 0:
        answer_text = "⚠️Еще нет новых не отмодерированных ответов"
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                      callback_data="main_admin")]])
        await callback.message.answer(text=answer_text,
                                      parse_mode="HTML",
                                      reply_markup=answer_kb
                                      )
    else:
        answers_count = len(answers)
        first_answer = answers[0]
        if first_answer[5] != "":
            answer_text = get_answer_text(first_answer)
            answer_kb = admin_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer(text=answer_text,
                                          parse_mode="HTML",
                                          reply_markup=answer_kb
                                          )
        elif first_answer[6] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = admin_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_photo(photo=first_answer[6],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[7] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = admin_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_video(video=first_answer[7],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[8] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = admin_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_audio(audio=first_answer[8],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[9] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = admin_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_document(document=first_answer[9],
                                                   caption=answer_text,
                                                   parse_mode="HTML",
                                                   reply_markup=answer_kb)
        elif first_answer[10] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = admin_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_voice(voice=first_answer[10],
                                                caption=answer_text,
                                                parse_mode="HTML",
                                                reply_markup=answer_kb)
        elif first_answer[11] != 0:
            answer_text = get_answer_caption(first_answer)
            answer_kb = admin_pagination_kb_answers(answers_count, 1, first_answer[0])
            await callback.message.answer_video_note(video_note=first_answer[11])
            await callback.message.answer(text=answer_text,
                                          reply_markup=answer_kb)


@router.callback_query(F.data.startswith('mod_a_page_'))
async def moderate_questions_page(callback: CallbackQuery):
    answers = select_moderating_answers()
    page = int(callback.data.split("_")[3])
    answer_count = len(answers)
    next_answer = answers[page - 1]
    if next_answer[5] != "":
        answer_text = get_answer_text(next_answer)
        answer_kb = admin_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer(text=answer_text,
                                      parse_mode="HTML",
                                      reply_markup=answer_kb
                                      )
    elif next_answer[6] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = admin_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_photo(photo=next_answer[6],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[7] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = admin_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_video(video=next_answer[7],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[8] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = admin_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_audio(audio=next_answer[8],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[9] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = admin_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_document(document=next_answer[9],
                                               caption=answer_text,
                                               parse_mode="HTML",
                                               reply_markup=answer_kb)
    elif next_answer[10] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = admin_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_voice(voice=next_answer[10],
                                            caption=answer_text,
                                            parse_mode="HTML",
                                            reply_markup=answer_kb)
    elif next_answer[11] != 0:
        answer_text = get_answer_caption(next_answer)
        answer_kb = admin_pagination_kb_answers(answer_count, page, next_answer[0])
        await callback.message.answer_video_note(video_note=next_answer[11])
        await callback.message.answer(text=answer_text,
                                      reply_markup=answer_kb)


@router.callback_query(F.data.startswith('ok_a_'))
async def ok_moderate_answers_page(callback: CallbackQuery, state: FSMContext):
    answer_id = int(callback.data.split("_")[2])
    await state.update_data(answer_id=answer_id)
    await callback.message.answer(text="⭐Оцените качество ответа от 0 до 100",
                                  reply_markup=ReplyKeyboardRemove())
    await state.set_state(RateAnswer.rating)


@router.message(RateAnswer.rating)
async def ok_moderate_answers_page(message: Message, state: FSMContext):
    await state.update_data(rating=message.text)
    user_data = await state.get_data()
    answer_id = user_data["answer_id"]
    answer = get_answer_by_id(answer_id)
    rating = int(user_data["rating"])
    question = get_question_by_id(answer[0][1])
    user_q = get_user_by_id(question[0][1])
    user_a = get_user_by_id(answer[0][2])
    if answer[0][13] == 0:  # если ответ не создан с помошью ИИ
        rating += 50
    moderate_answer(answer_id, rating)
    if user_q[0][7] == 1:
        await bot.send_message(chat_id=user_q[0][1], text=f"У вас новый ответ от пользователя @{user_a[0][2]}!")
    await bot.send_message(chat_id=answer[0][2],
                           text=f"✅Ваш ответ под номером {answer_id} одобрен администратором!")
    new_rating = user_a[0][6] + rating + 50
    update_user_rating(user_a[0][0], new_rating)
    update_user_rating(user_q[0][0], user_q[0][6] + 50)
    await message.answer(text="✅Ответ одобрен успешно!",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                                       callback_data="main_admin")]]))
    await state.clear()


@router.callback_query(F.data.startswith('not_a_'))
async def not_moderate_answer_page(callback: CallbackQuery, state: FSMContext):
    answer_id = int(callback.data.split("_")[2])
    await state.update_data(answer_id=answer_id)
    await callback.message.answer(text="✍️Напишите причину отказа в публикации",
                                  reply_markup=ReplyKeyboardRemove())
    await state.set_state(RejectAnswer.reason)


@router.message(RejectAnswer.reason)
async def not_moderate_answer_page(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    user_data = await state.get_data()
    answer_id = user_data["answer_id"]
    answer = get_answer_by_id(answer_id)
    await bot.send_message(chat_id=answer[0][2],
                           text=f"❌Ваш ответ под номером {answer_id} отклонен администратором!\n"
                                f"Причина: {user_data['reason']}")
    not_moderate_answer(answer_id)
    await message.answer(text="✅Ответ отклонен успешно!",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                                       callback_data="main_admin")]]))
    await state.clear()


@router.callback_query(F.data == "admin_mailing")
async def admin_mail(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="✍️Введите текст рассылки",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(MailAdmin.text)


@router.message(MailAdmin.text)
async def admin_mail(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(
        text="⏰Введите время отправки: сейчас ИЛИ дату и время отправки в формате 12:00 01.01.2024",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(MailAdmin.timedate)


@router.message(MailAdmin.timedate)
async def admin_mail(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
    await state.update_data(timedate=message.text)
    user_data = await state.get_data()
    if user_data["timedate"] == "сейчас":
        users = get_all_users()
        for user in users:
            try:
                await bot.send_message(chat_id=user[1],
                                   text=user_data["text"])
            except:
                pass
        await message.answer(text="✅Рассылка создана успешно!",
                             reply_markup=InlineKeyboardMarkup(
                                 inline_keyboard=[
                                     [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                                           callback_data="main_admin")]]))
    else:
        try:
            ins_time = user_data["timedate"].split(" ")[0]
            ins_date = user_data["timedate"].split(" ")[1]
            hours = ins_time.split(":")[0]
            minutes = ins_time.split(":")[1]
            year = ins_date.split(".")[2]
            month = ins_date.split(".")[1]
            day = ins_date.split(".")[0]
            apscheduler.add_job(send_notification, trigger="date", run_date=datetime(int(year), int(month),
                                                                                     int(day), int(hours),
                                                                                     int(minutes), 0),
                                kwargs={"text": user_data["text"], "bot": bot})
            await message.answer(text="✅Рассылка создана успешно!",
                                 reply_markup=InlineKeyboardMarkup(
                                     inline_keyboard=[
                                         [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                                               callback_data="main_admin")]]))
        except:
            await message.answer(text="❌Неверный формат даты или времени!",
                                 reply_markup=InlineKeyboardMarkup(
                                     inline_keyboard=[
                                         [InlineKeyboardButton(text=f"🏠На главную админ-панели",
                                                               callback_data="main_admin")]]))


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )


@router.callback_query(F.data == "main_admin")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        text="⚙️Добро пожаловать в админ-панель!\n" \
             "📝Здесь Вы можете одобрить или отклонить новые вопросы " \
             "и ответы, а также оформить рассылку для всех пользователей данного бота.\n" \
             "👉Выберите, с чего начать:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"❓Вопросы",
                                      callback_data="moderate_questions")],
                [InlineKeyboardButton(text=f"💬Ответы",
                                      callback_data="moderate_answers")],
                [InlineKeyboardButton(text=f"📩Создать рассылку",
                                      callback_data="admin_mailing")],
                [InlineKeyboardButton(text=f"🏠На главную",
                                      callback_data="main")]])
    )
