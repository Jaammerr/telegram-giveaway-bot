from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bt_admin_create_give = InlineKeyboardButton('Создать розыгрыш', callback_data='admin_gives')
bt_admin_created_gives = InlineKeyboardButton('Созданные розыгрыши', callback_data='admin_created_gives')
bt_admin_started_gives = InlineKeyboardButton('Активные розыгрыши', callback_data='admin_started_gives')

kb_admin_menu = InlineKeyboardMarkup().add(bt_admin_create_give, bt_admin_created_gives).add(bt_admin_started_gives)
