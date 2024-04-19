from aiogram.types import InlineKeyboardMarkup


def my_pagination_kb_answers(data_length: int, page: int, answer_id: int) -> InlineKeyboardMarkup:
    kb = {'inline_keyboard': []}
    buttons = []
    if page > 1:
        buttons.append({'text': '⬅', 'callback_data': f'my_a_page_{page - 1}'})
    buttons.append({'text': f'{page}/{data_length}', 'callback_data': 'none'})
    if page < data_length:
        buttons.append({'text': '➡', 'callback_data': f'my_a_page_{page + 1}'})
    kb['inline_keyboard'].append(buttons)
    kb['inline_keyboard'].append([{'text': '✏️Редактировать', 'callback_data': f'edit_a_{answer_id}'}])
    kb['inline_keyboard'].append([{'text': '🗑️Удалить', 'callback_data': f'delete_a_{answer_id}'}])
    kb['inline_keyboard'].append([{'text': '📊Проголосовать', 'callback_data': f'vote_a_{answer_id}'}])
    kb['inline_keyboard'].append([{'text': '🏠На главную', 'callback_data': 'main'}])
    return kb
