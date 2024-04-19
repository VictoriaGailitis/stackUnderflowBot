from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import bot
from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from db import get_user_by_id, update_user_answer_mailing, update_user_tags_mailing

from states.subscribing_tags import SubscribeTag

from handlers.schedule_handler import send_new_questions

router = Router()


@router.callback_query(F.data == "get_mailing")
async def get_mailing(callback: CallbackQuery):
    await callback.message.answer(text="👉Выберите тип рассылки",
                                  parse_mode="HTML",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(
                                              text=f"💬Рассылка уведомлений о новых ответах на ваши вопросы",
                                              callback_data="mail_answer")],
                                          [InlineKeyboardButton(text=f"🔖Рассылка новых вопросов по тегам",
                                                                callback_data="mail_tags")],
                                          [InlineKeyboardButton(text=f"🏠На главную",
                                                                callback_data="main")]])
                                  )


@router.callback_query(F.data == "mail_answer")
async def page(callback: CallbackQuery):
    user = get_user_by_id(callback.from_user.id)
    if user[0][7] == 0:
        answer_text = "❗Вы не подписаны на рассылку уведомлений о новых ответах на Ваши вопросы. Вы можете оформить ее" \
                      " по кнопке ниже👇🏻"
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔔Подписаться на рассылку",
                                      callback_data="sub_answers")],
                [InlineKeyboardButton(text=f"🏠На главную",
                                      callback_data="main")]])
    else:
        answer_text = "✅Вы уже подписаны на рассылку уведомлений о новых ответах на Ваши вопросы." \
                      " Вы можете отменить ее по кнопке ниже👇🏻"
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"❌Отписаться от рассылки",
                                      callback_data="cancel_answers")],
                [InlineKeyboardButton(text=f"🏠На главную",
                                      callback_data="main")]])
    await callback.message.answer(text=answer_text,
                                  parse_mode="HTML",
                                  reply_markup=answer_kb)


@router.callback_query(F.data == "sub_answers")
async def page(callback: CallbackQuery):
    user = get_user_by_id(callback.from_user.id)
    update_user_answer_mailing(user[0][1], 1)
    await callback.message.answer(text="✅Вы успешно подписались на рассылку!",
                                  parse_mode="HTML",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]]))


@router.callback_query(F.data == "cancel_answers")
async def page(callback: CallbackQuery):
    user = get_user_by_id(callback.from_user.id)
    update_user_answer_mailing(user[0][1], 0)
    await callback.message.answer(text="✅Вы успешно отказались от рассылки!",
                                  parse_mode="HTML",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]]))


@router.callback_query(F.data == "mail_tags")
async def page(callback: CallbackQuery):
    user = get_user_by_id(callback.from_user.id)
    if user[0][8] == "" or user[0][8] is None:
        answer_text = "❗Вы не подписаны на рассылку уведомлений о новых вопросах по выбранным тегам." \
                      "Вы можете оформить ее по кнопке ниже👇🏻"
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔔Подписаться на рассылку",
                                      callback_data="sub_tags")],
                [InlineKeyboardButton(text=f"🏠На главную",
                                      callback_data="main")]])
    else:
        answer_text = "✅Вы уже подписаны на рассылку уведомлений о новых вопросах по данным тегам: " \
                      f"{user[0][8]}." \
                      " Вы можете отменить ее или изменить по кнопкам ниже👇🏻"
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"❌Отписаться от рассылки",
                                      callback_data="cancel_tags")],
                [InlineKeyboardButton(text=f"✏️Редактировать свою рассылку",
                                      callback_data="sub_tags")],
                [InlineKeyboardButton(text=f"🏠На главную",
                                      callback_data="main")]])
    await callback.message.answer(text=answer_text,
                                  parse_mode="HTML",
                                  reply_markup=answer_kb)


@router.callback_query(F.data == "sub_tags")
async def page(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id)
    await callback.message.answer(
        text="🏷️Напишите один или несколько тегов",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SubscribeTag.tags)


@router.message(SubscribeTag.tags)
async def page(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    await message.answer(
        text="⏰Введите интервал отправки уведомлений в формате 1 нед ИЛИ 5 дн ИЛИ 12 ч ИЛИ 30 мин ИЛИ 45 сек",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SubscribeTag.time)


@router.message(SubscribeTag.time)
async def page(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
    await state.update_data(time=message.text)
    user_data = await state.get_data()
    if user_data["time"].split(" ")[1] == "нед":
        apscheduler.add_job(send_new_questions, trigger="interval", week=int(user_data["time"].split(" ")[0]),
                            kwargs={"user_id": user_data["user_id"], "bot": bot})
        answer_text = "✅ Вы успешно подписались на рассылку!"
        update_user_tags_mailing(user_data["user_id"], user_data["time"], user_data["tags"])
    elif user_data["time"].split(" ")[1] == "дн":
        apscheduler.add_job(send_new_questions, trigger="interval", day=int(user_data["time"].split(" ")[0]),
                            kwargs={"user_id": user_data["user_id"], "bot": bot})
        answer_text = "✅ Вы успешно подписались на рассылку!"
        update_user_tags_mailing(user_data["user_id"], user_data["time"], user_data["tags"])
    elif user_data["time"].split(" ")[1] == "ч":
        apscheduler.add_job(send_new_questions, trigger="interval", hours=int(user_data["time"].split(" ")[0]),
                            kwargs={"user_id": user_data["user_id"], "bot": bot})
        answer_text = "✅ Вы успешно подписались на рассылку!"
        update_user_tags_mailing(user_data["user_id"], user_data["time"], user_data["tags"])
    elif user_data["time"].split(" ")[1] == "мин":
        apscheduler.add_job(send_new_questions, trigger="interval", minutes=int(user_data["time"].split(" ")[0]),
                            kwargs={"user_id": user_data["user_id"], "bot": bot})
        answer_text = "✅ Вы успешно подписались на рассылку!"
        update_user_tags_mailing(user_data["user_id"], user_data["time"], user_data["tags"])
    elif user_data["time"].split(" ")[1] == "сек":
        apscheduler.add_job(send_new_questions, trigger="interval", seconds=int(user_data["time"].split(" ")[0]),
                            kwargs={"user_id": user_data["user_id"], "bot": bot})
        answer_text = "✅ Вы успешно подписались на рассылку!"
        update_user_tags_mailing(user_data["user_id"], user_data["time"], user_data["tags"])
    else:
        answer_text = "❌ Неверный формат временного интервала!"
    answer_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
    await message.answer(
        text=answer_text,
        reply_markup=answer_kb
    )


@router.callback_query(F.data == "cancel_tags")
async def page(callback: CallbackQuery, apscheduler: AsyncIOScheduler):
    user = get_user_by_id(callback.from_user.id)
    update_user_tags_mailing(user[0][1], "", "")
    for job in apscheduler.get_jobs():
            job.remove()
    await callback.message.answer(text="✅Вы успешно отказались от рассылки!",
                                  parse_mode="HTML",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]]))


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )
