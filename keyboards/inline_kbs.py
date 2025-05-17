from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from decouple import config

admins = [admin_id for admin_id in config('ADMINS').split(',')]
get_home = InlineKeyboardButton(text="✨ Главное меню", callback_data='back_home')


def register_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="✍🏻 Регистрация", callback_data='reg')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def get_to_main_menu():
    inline_kb_list = [
        [get_home]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def cancel_or_get_to_main_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="❌ Отменить", callback_data='make_order'),
         get_home]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def main_menu_kb(user_telegram_id: str):
    inline_kb_list = [
        [InlineKeyboardButton(text="🥗 Сделать заказ", callback_data='make_order')],
        [InlineKeyboardButton(text="📝 Мой заказ", callback_data='my_order'),
         InlineKeyboardButton(text="🍽 Меню", callback_data='current_menu')]
    ]
    if user_telegram_id in admins:
        inline_kb_list = [[InlineKeyboardButton(text="Список всех заказавших 📝", callback_data='admin')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def order_variants():
    inline_kb_list = [
        [InlineKeyboardButton(text="🍳 Завтрак", callback_data='ord_1'),
         InlineKeyboardButton(text="🍲 Обед", callback_data='ord_2'),
         InlineKeyboardButton(text="🍎 Полдник", callback_data='ord_3')],
        [InlineKeyboardButton(text="🍳🍝 Завтрак + обед", callback_data='ord_4')],
         [InlineKeyboardButton(text="🥞🍓 Завтрак + полдник", callback_data='ord_5')],
         [InlineKeyboardButton(text="🍜🍪 Обед + полдник", callback_data='ord_6')],
        [InlineKeyboardButton(text="🍳🍲🍰 Завтрак + обед + полдник", callback_data='ord_7')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def my_order():
    inline_kb_list = [
        [InlineKeyboardButton(text="❌ Отменить заказ", callback_data='delete_order'),
         get_home]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def get_out_after_cancel():
    inline_kb_list = [
        [get_home,
         InlineKeyboardButton(text="🥗 Сделать заказ", callback_data='make_order')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)