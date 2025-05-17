from datetime import timedelta

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from faker import Faker
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker

from create_bot import bot
from db_work.db_commands import *
from keyboards.inline_kbs import *

start_router = Router()

eng = create_engine('sqlite:///data/list_of_students.db')
Session = sessionmaker(bind=eng)
session = Session()

@start_router.message(F.text == '/help')
async def cmd_help(message: Message):
    await message.answer('💬 <b>Нужна помощь? Мы на связи!</b>\n\n'
                         'Если у тебя возникли вопросы или проблемы, пиши создателю ЛанчБота 👉 @by_gelya',
                         reply_markup=get_to_main_menu())

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    if not session.query(exists().where(User.username == message.from_user.username)).scalar():
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
    cancel_order(call.from_user.username)
    ords = int(call.data[4:])
    insert_info_orders(call.from_user.username, ords)
    await call.message.answer('Отлично! Куда дальше? 👀', reply_markup=cancel_or_get_to_main_menu())
    await call.answer()

@start_router.callback_query(F.data == 'current_menu')
async def menu_showing(call: CallbackQuery):
    file = FSInputFile(path='all_media/menu.docx')
    await call.message.answer('Сейчас пришлю файлик! Нужно немного подождать 💌')
    await call.answer()
    await call.message.answer_document(document=file, reply_markup=get_to_main_menu(),
                                    caption='Лови! 🙌🏻')


@start_router.callback_query(F.data == 'my_order')
async def show_order(call: CallbackQuery):
    now = datetime.now()
    if now.hour > 16:
        date = now + timedelta(days=1)
    else:
        date = now
    date = date.strftime("%d.%m.%Y")
    user_name = str(call.from_user.first_name)
    if get_active_orders(call.from_user.username) != 'У вас нет активных заказов! 🍽':
        order = str(get_active_orders(call.from_user.username)[0][1])
    else:
        order = str(get_active_orders(call.from_user.username))
    await call.message.answer(f'<i>Вот твой заказ на {date}, {user_name}!</i> 🤗\n\n'
                              f'<code>{order}</code> \n\n'
                              '🤔 <b>Хочешь отменить свой заказ, потому что не пойдешь в школу, или понял, не хочешь есть?</b> Жми кнопку "Отменить заказ"!\n\n'
                              '🤳🏼 <b>Передумал насчёт своего заказа?</b> Снова сделай заказ, он изменится автоматически!',
                              reply_markup=my_order())
    await call.answer()


@start_router.callback_query(F.data == 'delete_order')
async def delete_order(call: CallbackQuery):
    cancel_order(call.from_user.username)
    await call.message.answer('Заказ удалён! 🥢', reply_markup=get_out_after_cancel())
    await call.answer()


@start_router.callback_query(F.data == 'admin')
async def admin_only(call: CallbackQuery):
    data = ex_classes()
    existing_classes = ''
    if data != 'Нет текущих заказов ❌':
        for i in range(len(data) - 1):
            if data[i][:3] == data[i + 1][:3]:
                existing_classes = '\n'.join(data)
            else:
                existing_classes = '\n\n'.join(data)
        print(existing_classes)
        # await call.message.answer(existing_classes)
        await call.message.answer('Вот список всех заказавших! 📋', reply_markup=get_to_main_menu())
        await call.answer()
    else:
        await call.message.answer('Нет текущих заказов ❌', reply_markup=get_to_main_menu())
        await call.answer()
