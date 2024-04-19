from aiogram.types import InlineKeyboardMarkup

def my_pagination_kb(data_length: int, page: int, question_id: str, isMine: int) -> InlineKeyboardMarkup:
    kb = {'inline_keyboard': []}
    buttons = []
    if page > 1:
        buttons.append({'text': '⬅', 'callback_data': f'my_page_{page - 1}'})
    buttons.append({'text': f'{page}/{data_length}', 'callback_data': 'none'})
    if page < data_length:
        buttons.append({'text': '➡', 'callback_data': f'my_page_{page + 1}'})
    kb['inline_keyboard'].append(buttons)
    if isMine == 1:
        kb['inline_keyboard'].append([{'text': '✏️Редактировать', 'callback_data': f'edit_q_{question_id}'}])
        kb['inline_keyboard'].append([{'text': '🗑️Удалить', 'callback_data': f'delete_q_{question_id}'}])
    kb['inline_keyboard'].append([{'text': '💬Просмотреть ответы', 'callback_data': f'see_answers_{question_id}'}])
    kb['inline_keyboard'].append([{'text': '✍🏻Ответить на вопрос', 'callback_data': f'answer_{question_id}'}])
    kb['inline_keyboard'].append([{'text': '📊Проголосовать', 'callback_data': f'vote_q_{question_id}'}])
    kb['inline_keyboard'].append([{'text': '🏠На главную', 'callback_data': 'main'}])
    return kb
