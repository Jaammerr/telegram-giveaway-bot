from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action


bt_admin_add_group_for_channel = InlineKeyboardButton('Добавить группу', callback_data='admin_add_group')
bt_admin_delete_channel = InlineKeyboardButton('Удалить канал', callback_data='admin_delete_channel')
kb_admin_manage_selected_channel = InlineKeyboardMarkup().add(bt_admin_add_group_for_channel).add(bt_admin_delete_channel).add(bt_admin_cancel_action)
