from db import select_user_mailing, get_user_by_id, delete_user_mailings, get_all_users


async def send_new_questions(user_id, bot):
    result = select_user_mailing(user_id)
    user = get_user_by_id(user_id)
    if len(result) == 0:
        await bot.send_message(chat_id=user_id, text=f"⏰ Уведомление о новых вопросах по тегам {user[0][8]}!\n"
                                                     f"😔К сожалению, новых вопросов по даннмы тегам за {user[0][9]} не было\n"
                                                     f"Вы можете изменить теги или интервал рассылки в "
                                                     f"соответствующем пункте меню.")
    else:
        await bot.send_message(chat_id=user_id, text=f"⏰ Уведомление о новых вопросах по тегам {user[0][8]}!\n"
                                                     f"🔥По данным тегам за {user[0][9]} появилось {len(result)} новых(й) вопросов(а)!\n"
                                                     f"😉Просмотреть Вы их можете во вкладке со всеми вопросами, "
                                                     f"либо в поиске.")
        delete_user_mailings(user_id)


async def send_notification(text, bot):
    users = get_all_users()
    for user in users:
        try:
            await bot.send_message(chat_id=user[1], text=f"🔔 Рассылка от администратора:\n"
                                                         f"{text}")
        except:
            pass
