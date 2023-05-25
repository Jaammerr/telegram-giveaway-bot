from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .cancel_action import bt_admin_cancel_action


bt_admin_show_statistic = InlineKeyboardButton('Статистика', callback_data='admin_show_statistic')
bt_admin_stop_give = InlineKeyboardButton('Остановить', callback_data='admin_stop_give')

kb_admin_active_gives = InlineKeyboardMarkup().add(bt_admin_show_statistic, bt_admin_stop_give).add(bt_admin_cancel_action)
