import sqlite3

from keyboards.inline_kbs import admins


def create_db():
    conn = sqlite3.connect('list_of_students.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, status int, name varchar(100), class varchar(2), liter varchar(2))')
    conn.commit()

def insert_info(user_telegram_id: str, name, grade, liter):
    conn = sqlite3.connect('list_of_students.sql')
    cur = conn.cursor()
    if user_telegram_id in admins:
        cur.execute('INSERT INTO users (status, name, class, liter) VALUES ("%s", "%s", "%s", "%s")' % ('2', name, grade, liter))
    else:
        cur.execute('INSERT INTO users (status, name, class, liter) VALUES ("%s", "%s", "%s", "%s")' % ('1', name, grade, liter))
    conn.commit()