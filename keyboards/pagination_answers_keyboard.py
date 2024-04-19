from aiogram.types import InlineKeyboardMarkup
from db import get_answers_by_question_id

def pagination_kb_answers(data_length: int, page: int, question_id: str, isMine: int) -> InlineKeyboardMarkup:
    kb = {'inline_keyboard': []}
    buttons = []
    answers = get_answers_by_question_id(question_id)
    answer_id = answers[page-1][0]
    if page > 1:
        buttons.append({'text': '⬅', 'callback_data': f'apage_{page - 1}_{question_id}'})
    buttons.append({'text': f'{page}/{data_length}', 'callback_data': 'none'})
    if page < data_length:
        buttons.append({'text': '➡', 'callback_data': f'apage_{page + 1}_{question_id}'})
    kb['inline_keyboard'].append(buttons)
    if isMine == 1:
        kb['inline_keyboard'].append([{'text': '✏️Редактировать', 'callback_data': f'edit_a_{answer_id}'}])
        kb['inline_keyboard'].append([{'text': '🗑️Удалить', 'callback_data': f'delete_a_{answer_id}'}])
    kb['inline_keyboard'].append([{'text': '📊Проголосовать', 'callback_data': f'vote_a_{answer_id}'}])
    kb['inline_keyboard'].append([{'text': '🏠На главную', 'callback_data': 'main'}])
    return kb
