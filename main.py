import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = Bot(token='7280605209:AAH6JW03UpB9qjUf9FRhwwLxlqVTIY7_uGg')
dp = Dispatcher()

status_buttons = types.InlineKeyboardMarkup()
pupil = types.InlineKeyboardButton(text='Ученик', callback_data='pupil')
teacher = types.InlineKeyboardButton(text='Учитель', callback_data='teacher')
status_buttons.add(pupil, teacher)


@dp.message(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    conn = sqlite3.connect('list_of_students.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, username varchar(100), name varchar(100), '
        'class varchar(3))')
    conn.commit()
    await message.answer("🍏Привет, друг!\n"
                         "Ты попал в *«ЛанчБот🥞»* – твоего помощника в школьном питании!\n"
                         "📅*Выбирай завтрак, обед или полдник* – и всё само запишется.\n"
                         "📋*Смотри свои заказы* в любое время.\n"
                         "⏰*Успевай отменить*, если передумал!\n"
                         "📝*Давай зарегистрируемся?* Это быстро!\n"
                         "👉Жми *«Регистрация»* и начинай пользоваться!\n"
                         "❓ *Есть вопросы?* Напиши /help, и я помогу!\n",
                         reply_markup=types.InlineKeyboardMarkup().add(
                             types.InlineKeyboardButton(text='Регистрация', callback_data='register')
                         ))


@dp.callback_query(F.text.contains('register'))
async def registration(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Вы учитель или ученик?', reply_markup=status_buttons)


@dp.callback_query(F.text.contains('pupil', 'teacher'))
async def status_giving(callback_query: types.CallbackQuery):
    await callback_query.answer('Назови, пожалуйста, свои ФИО. Хотим познакомиться 👐')


if __name__ == '__main__':
    dp.start_polling(bot)
