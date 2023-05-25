from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action


bt_admin_add_captcha_for_give = InlineKeyboardButton('Да', callback_data='admin_add_captcha_for_give')
bt_admin_not_add_captcha_for_give = InlineKeyboardButton('Нет', callback_data='admin_not_add_captcha_for_give')

kb_admin_add_captcha_for_give = InlineKeyboardMarkup().add(bt_admin_add_captcha_for_give, bt_admin_not_add_captcha_for_give).add(bt_admin_cancel_action)
