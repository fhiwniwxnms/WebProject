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

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('list_of_students.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(100), class varchar(3), password varchar(50))')
    conn.commit()

    register = telebot.types.InlineKeyboardMarkup()
    register.add(telebot.types.InlineKeyboardButton('✍Регистрация', callback_data='users'))
    bot.send_message(message.chat.id, '🍏 Привет, друг!\n'
                                      'Ты попал в *«ЛанчБот🥞»* – твоего помощника в школьном питании!\n'
                                      '📅*Выбирай завтрак, обед или полдник* – и всё с**амо запишется.'
                                      '📋*Смотри свои заказы* в любое время.'
                                      '⏰*Успевай отменить*, если передумал!\n'
                                      '📝*Давай зарегистрируемся?* Это быстро!\n'
                                      '👉Жми *«Регистрация»* и начинай пользоваться!\n'
                                      '❓ *Есть вопросы?* Напиши /help, и я помогу!\n'
                                      '🍕 *Пусть в столовой всегда будет вкусно!*', reply_markup=register)
    cur.close()
    conn.close()


@bot.callback_query_handler(func=lambda call: True)
def register(call):
    user_class = telebot.types.InlineKeyboardMarkup()
    user_class.add(telebot.types.InlineKeyboardButton('Учитель', callback_data='users'))
    user_class.add(telebot.types.InlineKeyboardButton('Ученик', callback_data='users'))
    bot.send_message(call.message.chat.id,'Вы учитель или ученик?', reply_markup=user_class)


bot.polling(none_stop=True)