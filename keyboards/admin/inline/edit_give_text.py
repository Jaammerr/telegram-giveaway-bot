from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bt_admin_edit_give_text = InlineKeyboardButton('Редактировать текст', callback_data='admin_edit_give_text')
bt_admin_continue_create_give = InlineKeyboardButton('Продолжить', callback_data='admin_continue_create_give')

kb_admin_edit_give_text = InlineKeyboardMarkup().add(bt_admin_edit_give_text).add(bt_admin_continue_create_give)
