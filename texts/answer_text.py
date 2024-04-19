from db import get_user_by_id

def get_answer_text(answer):
    user = get_user_by_id(answer[2])
    return f"\n💬Ответ №{answer[0]} от : @{user[0][2]}\n" \
           f"📜Текст ответа: {answer[5]}\n" \
           f"📊Голосов: {answer[14]}\n" \
           f"📅Дата и время отправки: {answer[4]}\n" \
           f"🤖Создан с помощью Тима: {'нет' if answer[13] == 0 else 'да'}\n"



def get_answer_caption(answer):
    user = get_user_by_id(answer[2])
    return f"\n💬Ответ №{answer[0]} от: @{user[0][2]}\n" \
           f"📊Голосов: {answer[14]}\n" \
           f"📅Дата и время отправки: {answer[4]}\n" \
           f"🤖Создан с помощью Тима: {'нет' if answer[13] == 0 else 'да'}\n"
