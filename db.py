import sqlite3

conn = sqlite3.connect('stackUnderflowDB.db', check_same_thread=False)
cursor = conn.cursor()


def insert_user(user_tg_id: int, username: str, user_first_name: str, user_last_name: str,
                isAdmin: int, user_rating: int, mail_answers: int, mail_tags: str):
    cursor.execute('INSERT OR IGNORE INTO users (user_tg_id, username, user_first_name, user_last_name,'
                   'isAdmin, user_rating, mail_answers, mail_tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_tg_id, username, user_first_name, user_last_name, isAdmin, user_rating,
                    mail_answers, mail_tags))
    conn.commit()


def insert_question(user_id: int, onModeration: int, date_posted: str, question_text: str,
                    question_photo_id: int, question_video_id: int, question_audio_id: int,
                    question_document_id: int, question_voice_id: int, question_video_note_id: int,
                    question_rating: int, isAI: int, tags: str, question_votes: int):
    cursor.execute('INSERT INTO questions (user_id, onModeration, date_posted, question_text, '
                   'question_photo_id, question_video_id, question_audio_id, '
                   'question_document_id, question_voice_id,'
                   'question_video_note_id, question_rating, isAI, tags, question_votes)'
                   'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_id, onModeration, date_posted, question_text, question_photo_id, question_video_id,
                    question_audio_id, question_document_id, question_voice_id,
                    question_video_note_id, question_rating, isAI, tags, question_votes))
    conn.commit()


def insert_answer(question_id: int, user_id: int, onModeration: int, date_posted: str, answer_text: str,
                  answer_photo_id: int, answer_video_id: int, answer_audio_id: int,
                  answer_document_id: int, answer_voice_id: int, answer_video_note_id: int,
                  answer_rating: int, isAI: int, answer_votes: int):
    cursor.execute('INSERT INTO answers (question_id, user_id, onModeration, date_posted,'
                   'answer_text, answer_photo_id, answer_video_id, answer_audio_id, '
                   'answer_document_id, answer_voice_id, answer_video_note_id, '
                   'answer_rating, isAI, answer_votes) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (question_id, user_id, onModeration, date_posted, answer_text,
                    answer_photo_id, answer_video_id, answer_audio_id,
                    answer_document_id, answer_voice_id, answer_video_note_id,
                    answer_rating, isAI, answer_votes))
    conn.commit()


def get_all_questions():
    sqlite_select_query = """SELECT * from questions WHERE onModeration = 0 ORDER BY question_votes DESC"""
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def get_all_users():
    sqlite_select_query = """SELECT * from users"""
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def get_user_by_id(user_id):
    cursor.execute("""SELECT * from users WHERE user_tg_id = ?""", (user_id,))
    return cursor.fetchall()


def get_question_by_id(question_id):
    cursor.execute("""SELECT * from questions WHERE question_id = ?""", (question_id,))
    return cursor.fetchall()


def get_answer_by_id(answer_id):
    cursor.execute("""SELECT * from answers WHERE answer_id = ?""", (answer_id,))
    return cursor.fetchall()


def get_answers_by_question_id(question_id):
    cursor.execute("""SELECT * from answers WHERE question_id = ? AND onModeration = 0 ORDER BY answer_votes DESC""",
                   (question_id,))
    return cursor.fetchall()


def insert_vote_question(user_id: int, question_id: str):
    cursor.execute("""SELECT * from votes_questions""")
    records = cursor.fetchall()
    for record in records:
        if record[1] == user_id and record[2] == int(question_id):
            raise ValueError("There is no jam. Sad bread.")
    cursor.execute('INSERT INTO votes_questions (user_id, question_id) VALUES (?, ?)',
                   (user_id, question_id))
    conn.commit()


def insert_vote_answer(user_id: int, answer_id: str):
    cursor.execute("""SELECT * from votes_answers""")
    records = cursor.fetchall()
    for record in records:
        if record[1] == user_id and record[2] == int(answer_id):
            raise ValueError("There is no jam. Sad bread.")
    cursor.execute('INSERT INTO votes_answers (user_id, answer_id) VALUES (?, ?)',
                   (user_id, answer_id))
    conn.commit()


def update_votes_question(question_id: int, votes: int):
    cursor.execute('UPDATE questions SET question_votes = ? WHERE question_id = ?',
                   (votes, question_id))
    conn.commit()


def update_votes_answer(answer_id: int, votes: int):
    cursor.execute('UPDATE answers SET answer_votes = ? WHERE answer_id = ?',
                   (votes, answer_id))
    conn.commit()


def select_questions_by_tags(tags):
    sqlite_select_query = f"SELECT * from questions WHERE onModeration = 0 AND tags LIKE '%{tags[0]}%'"
    for i in range(1, len(tags)):
        sqlite_select_query += f" OR tags LIKE '%{tags[i]}%'"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def update_question(question_id: int, onModeration: int, date_posted: str, question_text: str,
                    question_photo_id: int, question_video_id: int, question_audio_id: int,
                    question_document_id: int, question_voice_id: int, question_video_note_id: int,
                    tags: str):
    cursor.execute('UPDATE questions SET onModeration = ?, date_posted = ?, question_text = ?, '
                   'question_photo_id = ?, question_video_id = ?, question_audio_id = ?, '
                   'question_document_id = ?, question_voice_id = ?, question_video_note_id = ?, '
                   'tags = ? WHERE question_id = ?',
                   (onModeration, date_posted, question_text, question_photo_id, question_video_id,
                    question_audio_id, question_document_id, question_voice_id,
                    question_video_note_id, tags, question_id))
    conn.commit()


def update_answer(answer_id: int, onModeration: int, date_posted: str, answer_text: str,
                  answer_photo_id: int, answer_video_id: int, answer_audio_id: int,
                  answer_document_id: int, answer_voice_id: int, answer_video_note_id: int):
    cursor.execute('UPDATE answers SET onModeration = ?, date_posted = ?, answer_text = ?, '
                   'answer_photo_id = ?, answer_video_id = ?, answer_audio_id = ?, '
                   'answer_document_id = ?, answer_voice_id = ?, answer_video_note_id = ? '
                   'WHERE answer_id = ?',
                   (onModeration, date_posted, answer_text, answer_photo_id, answer_video_id,
                    answer_audio_id, answer_document_id, answer_voice_id,
                    answer_video_note_id, answer_id))
    conn.commit()


def update_user_answer_mailing(user_id, mail_answers):
    cursor.execute('UPDATE users SET mail_answers = ? WHERE user_tg_id = ?',
                   (mail_answers, user_id))
    conn.commit()


def update_user_tags_mailing(user_id, mail_time, mail_tags):
    cursor.execute('UPDATE users SET mail_tags = ?, mail_time = ? WHERE user_tg_id = ?',
                   (mail_tags, mail_time, user_id))
    conn.commit()


def select_user_mailing(user_id):
    sqlite_select_query = f"SELECT * from mailings WHERE user_id = {user_id}"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def delete_user_mailings(user_id):
    sqlite_delete_query = f"DELETE from mailings WHERE user_id = {user_id}"
    cursor.execute(sqlite_delete_query)
    conn.commit()


def insert_new_mailing(user_id, question_id):
    cursor.execute('INSERT OR IGNORE INTO mailings (user_id, question_id) VALUES (?, ?)',
                   (user_id, question_id))
    conn.commit()


def get_last_question():
    sqlite_select_query = f"SELECT * from questions ORDER BY question_id DESC"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def get_user_answers(user_id):
    sqlite_select_query = f"SELECT * from answers WHERE onModeration = 0 AND user_id = {user_id}"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def get_user_questions(user_id):
    sqlite_select_query = f"SELECT * from questions WHERE onModeration = 0 AND user_id = {user_id}"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def select_moderating_questions():
    sqlite_select_query = "SELECT * from questions WHERE onModeration = 1"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def select_moderating_answers():
    sqlite_select_query = "SELECT * from answers WHERE onModeration = 1"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()


def moderate_question(question_id, question_rating):
    cursor.execute('UPDATE questions SET onModeration = 0, question_rating = ? WHERE question_id = ?',
                   (question_rating, question_id))
    conn.commit()


def moderate_answer(answer_id, answer_rating):
    cursor.execute('UPDATE answers SET onModeration = 0, answer_rating = ? WHERE answer_id = ?',
                   (answer_rating, answer_id))
    conn.commit()


def not_moderate_question(question_id):
    sqlite_delete_query = f"DELETE from questions WHERE question_id = {question_id}"
    cursor.execute(sqlite_delete_query)
    conn.commit()


def not_moderate_answer(answer_id):
    sqlite_delete_query = f"DELETE from answers WHERE answer_id = {answer_id}"
    cursor.execute(sqlite_delete_query)
    conn.commit()

def update_user_rating(user_id, user_rating):
    cursor.execute('UPDATE users SET user_rating = ? WHERE user_id = ?',
                   (user_rating, user_id))
    conn.commit()

def select_users_rating():
    sqlite_select_query = "SELECT * from users ORDER BY user_rating DESC"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()

def get_my_questions(user_id):
    sqlite_select_query = f"SELECT * from questions WHERE user_id = {user_id}"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()

def get_my_answers(user_id):
    sqlite_select_query = f"SELECT * from answers WHERE user_id = {user_id}"
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()