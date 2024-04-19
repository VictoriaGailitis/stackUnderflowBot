from aiogram.types import InlineKeyboardMarkup


def admin_questions_pagination_kb(data_length: int, page: int, question_id: str) -> InlineKeyboardMarkup:
    kb = {'inline_keyboard': []}
    buttons = []
    if page > 1:
        buttons.append({'text': '⬅', 'callback_data': f'mod_q_page_{page - 1}'})
    buttons.append({'text': f'{page}/{data_length}', 'callback_data': 'none'})
    if page < data_length:
        buttons.append({'text': '➡', 'callback_data': f'mod_q_page_{page + 1}'})
    kb['inline_keyboard'].append(buttons)
    kb['inline_keyboard'].append([{'text': '💬Одобрить вопрос', 'callback_data': f'ok_q_{question_id}'}])
    kb['inline_keyboard'].append([{'text': '✍🏻Отклонить вопрос', 'callback_data': f'not_q_{question_id}'}])
    kb['inline_keyboard'].append([{'text': '🏠На главную админ-панели', 'callback_data': 'main_admin'}])
    return kb
