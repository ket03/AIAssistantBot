# БД
# Создать
# Добавить пользователя, если его нет в таблице
# При оплате изменить счетчик stars
# При успешной оплате обнулить stars и увеличить count

import sqlite3

connection = sqlite3.connect('id.db', check_same_thread=False)
cursor = connection.cursor()

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER,
            counter INTEGER,
            model TEXT NOT NULL,
            stars INTEGER
        )''')
    connection.commit()


def add_user(user_id):
    cursor.execute('''
        INSERT OR IGNORE INTO Users (id, counter, model, stars) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, 0, 'gpt-4o', 0))
    connection.commit()


def change_value_stars(user_id, new_stars):
    cursor.execute('''
        UPDATE Users
        SET stars = ?
        WHERE id = ?
    ''', (new_stars, user_id))
    connection.commit()


def change_value_counter(user_id, new_counter):
    cursor.execute('''
        UPDATE Users
        SET counter = counter + ?
        WHERE id = ?
    ''', (new_counter, user_id))
    connection.commit()


def set_stars_to_zero(user_id):
    cursor.execute('''
        UPDATE Users
        SET stars = ?
        WHERE id = ?
    ''', (0, user_id))
    connection.commit()


def get_value_counter(user_id):
    cursor.execute('''
        SELECT counter
        FROM Users
        WHERE id = ?
    ''', (user_id,))
    current_counter = cursor.fetchone()[0]
    return current_counter


def is_enough_counter(current_model, current_counter):
    if current_model == 'gpt-4o':
        if current_counter >= 1:
            return True
    elif current_model == 'dalle':
        if current_counter >= 5:
            return True
    return False


def get_value_model(user_id):
    cursor.execute('''
        SELECT model
        FROM Users
        WHERE id = ?
    ''', (user_id,))
    current_model = cursor.fetchone()[0]
    return current_model


def sub_value_counter(user_id, current_model):
    if current_model == 'dalle':
        cursor.execute('''
            UPDATE Users
            SET counter = counter - 5
            WHERE id = ?
        ''', (user_id, ))
        connection.commit()

    if current_model == 'gpt-4o':
        cursor.execute('''
            UPDATE Users
            SET counter = counter - 1
            WHERE id = ?
        ''', (user_id,))
        connection.commit()


def change_value_model(user_id, new_model):
    cursor.execute('''
        UPDATE Users
        SET model = ?
        WHERE id = ?
    ''', (new_model, user_id))
    connection.commit()


def get_value_stars(user_id):
    cursor.execute('''
        SELECT stars
        FROM Users
        WHERE id = ?
    ''', (user_id,))
    return int(cursor.fetchone()[0])


def select_table():
    cursor.execute('''
        SELECT *
        FROM Users
    ''')
    print(cursor.fetchone())
