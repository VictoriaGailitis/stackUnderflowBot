from db import get_user_by_id


def add_hashtag(string):
    return "#" + string


def get_question_text(question):
    user = get_user_by_id(question[1])
    tags = list(map(add_hashtag, question[13].split(' ')))
    return f"\n🙋Вопрос №{question[0]} от : @{user[0][2]}\n" \
           f"📜Текст вопроса: {question[4]}\n" \
           f"🏷️️Теги: {' '.join(tag for tag in tags)}\n" \
           f"📊Голосов: {question[14]}\n" \
           f"📅Дата и время отправки: {question[3]}\n" \
           f"🤖Создан с помощью Тима: {'нет' if question[12] == 0 else 'да'}\n"



def get_question_caption(question):
    user = get_user_by_id(question[1])
    tags = list(map(add_hashtag, question[13].split(' ')))
    return f"\n🙋Вопрос №{question[0]} от : @{user[0][2]}\n" \
           f"🏷️️Теги: {' '.join(tag for tag in tags)}\n" \
           f"📅Дата и время отправки: {question[3]}\n" \
           f"📊Голосов: {question[14]}\n" \
           f"🤖Создан с помощью Тима: {'нет' if question[12] == 0 else 'да'}\n"
