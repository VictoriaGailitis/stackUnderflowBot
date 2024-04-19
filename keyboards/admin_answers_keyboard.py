from aiogram.types import InlineKeyboardMarkup


def admin_pagination_kb_answers(data_length: int, page: int, answer_id: int) -> InlineKeyboardMarkup:
    kb = {'inline_keyboard': []}
    buttons = []
    if page > 1:
        buttons.append({'text': '⬅', 'callback_data': f'mod_a_page_{page - 1}'})
    buttons.append({'text': f'{page}/{data_length}', 'callback_data': 'none'})
    if page < data_length:
        buttons.append({'text': '➡', 'callback_data': f'mod_a_page_{page + 1}'})
    kb['inline_keyboard'].append(buttons)
    kb['inline_keyboard'].append([{'text': '💬Одобрить ответ', 'callback_data': f'ok_a_{answer_id}'}])
    kb['inline_keyboard'].append([{'text': '✍🏻Отклонить ответ', 'callback_data': f'not_a_{answer_id}'}])
    kb['inline_keyboard'].append([{'text': '🏠На главную админ-панели', 'callback_data': 'main_admin'}])
    return kb
