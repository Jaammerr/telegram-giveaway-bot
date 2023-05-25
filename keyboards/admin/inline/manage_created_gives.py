from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action


bt_admin_start_give = InlineKeyboardButton('Запустить', callback_data='admin_start_give')
bt_admin_delete_give = InlineKeyboardButton('Удалить', callback_data='admin_delete_give')
bt_admin_manage_channels = InlineKeyboardButton('Каналы', callback_data='admin_manage_channels')
bt_admin_change_over_date = InlineKeyboardButton('Изменить дату окончания', callback_data='admin_change_over_date')
kb_admin_manage_created_gives = InlineKeyboardMarkup().add(bt_admin_start_give, bt_admin_delete_give).add(bt_admin_manage_channels).add(bt_admin_change_over_date).add(
    bt_admin_cancel_action
)
