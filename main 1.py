import telebot
from telebot import types, callback_data
import sqlite3
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot('7280605209:AAH6JW03UpB9qjUf9FRhwwLxlqVTIY7_uGg')
status_keyboard = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('Ученик', callback_data='1'),
    telebot.types.InlineKeyboardButton('Учитель', callback_data='2'))


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('list_of_students.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, status int, name varchar(100), class varchar(3))')
    conn.commit()

    register = telebot.types.InlineKeyboardMarkup()
    register.add(telebot.types.InlineKeyboardButton('✍Регистрация', callback_data='users'))
    bot.send_message(
        message.chat.id, "🍏Привет, друг\!"
                         "Ты попал в *«ЛанчБот🥞»* – твоего помощника в школьном питании\!"
                         "📅*Выбирай завтрак, обед или полдник* – и всё само запишется\."
                         "📋*Смотри свои заказы* в любое время\."
                         "⏰*Успевай отменить*, если передумал\!"
                         "📝*Давай зарегистрируемся\?* Это быстро\!"
                         "👉Жми *«Регистрация»* и начинай пользоваться\!"
                         "❓ *Есть вопросы\?* Напиши /help, и я помогу\!",
        parse_mode='MarkdownV2', reply_markup=register
    )
    cur.close()
    conn.close()


@bot.callback_query_handler(func=lambda call: True)
def classification_of_users(call: types.CallbackQuery):
    bot.send_message(call.message.chat.id, 'Вы учитель или ученик?', reply_markup=status_keyboard)
    if call.data == '1':
        logging.info(call.data)
        # bot.register_next_step_handler(call.message, pupil)
    if call.data == '2':
        logging.info(call.data)
        teacher(call)

# Сделать функции, возращающие значения имени, класса и тп

def pupil(call: types.CallbackQuery):
    logging.info(call)
    bot.send_message(call.message.chat.id, 'Назови, пожалуйста, свои ФИО. Хотим познакомиться 👐')

    name = call.message.text.strip()
    bot.send_message(call.message.chat.id, 'Введи свой класс с литерой класса. Пример: "11А"')

    clas = call.message.text.strip().upper()

    conn = sqlite3.connect('list_of_students.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (status, name, class) VALUES ("%s", "%s", "%s")' % ('1', name, clas))
    conn.commit()

    bot.register_next_step_handler(call.message, main)


def teacher(call: types.CallbackQuery):
    bot.send_message(call.message.chat.id, 'Назовите, пожалуйста, свои ФИО')

    name = call.message.text.strip()
    bot.send_message(call.message.chat.id, 'Каким классом вы руководите? Напишите цифру и литеру класса. Пример: "11А"')

    clas = call.message.text.strip().upper()

    conn = sqlite3.connect('list_of_students.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (status, name, class) VALUES ("%s", "%s", "%s")' % ('2', name, clas))
    conn.commit()

    bot.register_next_step_handler(call.message, main)


@bot.callback_query_handler(func=lambda call: True)
def main(call: types.CallbackQuery):
    pass


bot.polling(none_stop=True)
