from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from faker import Faker

from create_bot import bot
from db_work.db_commands import *
from keyboards.inline_kbs import *

start_router = Router()
reg_users = [user_username for user_username in config('REG_USERS').split(',')]

questions = {
    1: {'qst': 'Столица Италии?', 'answer': 'Рим'},
    2: {'qst': 'Сколько континентов на Земле?', 'answer': 'Семь'},
    3: {'qst': 'Самая длинная река в мире?', 'answer': 'Нил'},
    4: {'qst': 'Какой элемент обозначается символом "O"?', 'answer': 'Кислород'},
    5: {'qst': 'Как зовут главного героя книги "Гарри Поттер"?', 'answer': 'Гарри Поттер'},
    6: {'qst': 'Сколько цветов в радуге?', 'answer': 'Семь'},
    7: {'qst': 'Какая планета третья от Солнца?', 'answer': 'Земля'},
    8: {'qst': 'Кто написал "Войну и мир"?', 'answer': 'Лев Толстой'},
    9: {'qst': 'Что такое H2O?', 'answer': 'Вода'},
    10: {'qst': 'Какой океан самый большой?', 'answer': 'Тихий океан'},
}

type_eat = {
    0: 'Ничего',
    1: 'Столица Италии?',
    2: 'Сколько континентов на Земле?',
    3: 'Самая длинная река в мире?',
    4: 'Какой элемент обозначается символом "O"?',
    5: 'Как зовут главного героя книги "Гарри Поттер"?',
    6: 'Сколько цветов в радуге?'
}


# @start_router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()',
#                          reply_markup=main_kb(message.from_user.id))
#
# @start_router.message(Command('start_2'))
# async def cmd_start(message: Message):
#     await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()',
#                          reply_markup=create_spec_kb())
#
# @start_router.message(F.text == '/start_3')
# async def cmd_start(message: Message):
#     await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!',
#                          reply_markup=create_rat())
#
# @start_router.message(F.text == 'Давай инлайн!')
# async def get_inline_btn_link(message: Message):
#     await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=get_inline_kb())
#
# @start_router.callback_query(F.data == 'get_person')
# async def send_random_person(call: CallbackQuery):
#     # await call.answer('Генерирую случайного пользователя')
#     user = Faker('ru_RU').name()
#     await call.message.answer(user)
#     await call.answer('Генерирую случайного пользователя', show_alert=False)
#
# @start_router.callback_query(F.data == 'back_home')
# async def get_back_home(call: CallbackQuery):
#     await call.message.answer('Обратно на главную',
#                          reply_markup=main_kb(call.message.from_user.id))
#     await call.answer('Возвращаю', show_alert=True)

# @start_router.callback_query(F.data.startswith('qst_'))
# async def cmd_start(call: CallbackQuery):
#     await call.answer()
#     qst_id = int(call.data.replace('qst_', ''))
#     qst_data = questions[qst_id]
#     msg_text = f'Ответ на вопрос {qst_data.get("qst")}\n\n' \
#                f'<b>{qst_data.get("answer")}</b>\n\n' \
#                f'Выбери другой вопрос:'
#     async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
#         await asyncio.sleep(2)
#         await call.message.answer(msg_text, reply_markup=create_qst_inline_kb(questions))


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.username not in reg_users:
        await message.answer('🍏Привет, друг!\n\n'
                             'Ты попал в <b>«ЛанчБот🥞»</b> – твоего помощника в школьном питании!\n\n'
                             '📅<b>Выбирай завтрак, обед или полдник</b> – и всё само запишется.\n'
                             '📋<b>Смотри свои заказы</b> в любое время.\n'
                             '⏰<b>Успевай отменить</b>, если передумал!\n\n'
                             '📝<b>Давай зарегистрируемся?</b> Это быстро!\n'
                             '👉Жми <b>«Регистрация»</b> и начинай пользоваться!\n\n'
                             '❓ <b>Есть вопросы?</b> Напиши /help, и я помогу!\n', reply_markup=register_kb())
    else:
        await message.answer('👋🏻 <b>Добро пожаловать в чат-бот по заказу школьной еды!</b>\n\n'
                             '🧃 <b>Хочешь заказать завтрак или обед?</b> Нажимай "Сделать заказ" и выбирай!\n'
                             '📋 <b>Смотри свои заказы</b> в любое время.\n'
                             '⏰ <b>Успевай отменить</b>, если передумал!\n'
                             '🍝 <b>Не знаешь, что сегодня подают в столовой?</b> Взгляни на меню!\n\n'
                             '❓ <b>Есть вопросы?</b> Напиши /help, и я помогу!\n'
                             '🍕 <i>Пусть в столовой всегда будет вкусно!</i>',
                             reply_markup=main_menu_kb(message.from_user.username))


@start_router.callback_query(F.data == 'reg')
async def get_user_info(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Назови, пожалуйста, свои ФИО. Хотим познакомиться 👐\n'
                                                 'Затем введи свой класс с литерой класса через пробел.\n'
                                                 f'Пример: "{Faker("ru_RU").name()} 11 А"')


@start_router.message(F.text)
async def next_step(message: Message):
    info = message.text.strip().split()
    username, name, grade, liter = message.from_user.username, f'{info[0]} {info[1]} {info[2]}', info[3], info[4]
    print(username, name, grade, liter)
    insert_info_users(username, name, grade, liter)
    await message.answer('Отлично! Погнали дальше?😉', reply_markup=get_to_main_menu())


@start_router.callback_query(F.data == 'back_home')
async def main_menu(call: CallbackQuery):
    await call.message.answer('👋🏻 <b>Добро пожаловать в чат-бот по заказу школьной еды!</b>\n\n'
                              '🧃 <b>Хочешь заказать завтрак или обед?</b> Нажимай "Сделать заказ" и выбирай!\n'
                              '📋 <b>Смотри свои заказы</b> в любое время.\n'
                              '⏰ <b>Успевай отменить</b>, если передумал!\n'
                              '🍝 <b>Не знаешь, что сегодня подают в столовой?</b> Взгляни на меню!\n\n'
                              '❓ <b>Есть вопросы?</b> Напиши /help, и я помогу!\n'
                              '🍕 <i>Пусть в столовой всегда будет вкусно!</i>',
                              reply_markup=main_menu_kb(call.from_user.username))
    await call.answer('Переходим в главное меню 💤', show_alert=False)


@start_router.callback_query(F.data == 'make_order')
async def make_order_qst(call: CallbackQuery):
    await call.message.answer('Какой у тебя заказ? 💁🏻‍♀️', reply_markup=order_variants())
    await call.answer()


@start_router.callback_query(F.data.startswith('ord_'))
async def make_order(call: CallbackQuery):
    ords = int(F.data[4:])
    insert_info_orders(call.from_user.username, ords)
    await call.message.answer('Отлично! Куда дальше? 👀', reply_markup=cancel_or_get_to_main_menu())
    await call.answer()
