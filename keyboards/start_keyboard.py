from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def start_kb():
    buttons = [
        [InlineKeyboardButton(text="📋Все вопросы", callback_data="see_all")],
        [InlineKeyboardButton(text="❓Задать вопрос", callback_data="leave_question")],
        [InlineKeyboardButton(text="🥇Рейтинг пользователей", callback_data="see_rating")],
        [InlineKeyboardButton(text="👥Авторы вопросов и ответов", callback_data="see_users")],
        [InlineKeyboardButton(text="📩Рассылки", callback_data="get_mailing")],
        [InlineKeyboardButton(text="🗂️Мои вопросы", callback_data="get_my_questions")],
        [InlineKeyboardButton(text="📂Мои ответы", callback_data="get_my_answers")],
        [InlineKeyboardButton(text="🔎Поиск по тегам", callback_data="search_tags")],
        [InlineKeyboardButton(text="⚙️Админ-панель", callback_data="admin")],
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb