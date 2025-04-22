from gc import callbacks
import telebot
from telebot import types
import sqlite3
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot('7280605209:AAH6JW03UpB9qjUf9FRhwwLxlqVTIY7_uGg')
name = ''
clas = ''
conn = sqlite3.connect('list_of_students.sql')
cur = conn.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(100), class varchar(3), password varchar(50))')
    conn.commit()

    bot.send_message(message.chat.id, 'Здравствуйте! Пройдите регистрацию.')
    bot.send_message(message.chat.id, 'Назовите ваше ФИО.')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id,
                     'Введите ваш класс с литерой класса. Пример: "11А". Если вы родитель, напишите в сообщении "РОД".')
    bot.register_next_step_handler(message, user_class)


def user_class(message):
    global clas
    clas = message.text.strip().upper()
    bot.send_message(message.chat.id, 'Введите пароль.')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    pw = message.text.strip()

    cur.execute('INSERT INTO users (name, class, password) VALUES ("%s", "%s", "%s")' % (name, clas, pw))
    conn.commit()

    bot.send_message(message.chat.id, 'Пользователь зарегестрирован!')


# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()
#
#     info = ''
#     for el in users:
#         info += f'Имя: {el[1]}, класс: {el[2]}\n'
#
#     bot.send_message(call.message.chat.id, info)


cur.close()
conn.close()
bot.polling(none_stop=True)