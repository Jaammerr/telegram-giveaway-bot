from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action


bt_admin_give_type_comments = InlineKeyboardButton('По комментариям', callback_data='admin_give_type_comments')
bt_admin_give_type_button = InlineKeyboardButton('По кнопке', callback_data='admin_give_type_button')

kb_admin_select_type_of_give = InlineKeyboardMarkup().add(bt_admin_give_type_comments, bt_admin_give_type_button).add(bt_admin_cancel_action)
