from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action


bt_admin_add_channel = InlineKeyboardButton('Добавить канал', callback_data='admin_add_channel')
bt_admin_active_channels = InlineKeyboardButton('Подключенные каналы', callback_data='admin_active_channels')

kb_admin_manage_channels = InlineKeyboardMarkup().add(bt_admin_add_channel).add(bt_admin_active_channels).add(bt_admin_cancel_action)
