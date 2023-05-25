from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action

bt_owner_active_gives = InlineKeyboardButton('Активные розыгрыши', callback_data='owner_active_gives')
kb_owner_menu = InlineKeyboardMarkup().add(bt_owner_active_gives)

bt_owner_change_winners = InlineKeyboardButton('Изменить победителей', callback_data='owner_change_winners')
bt_owner_statistic = InlineKeyboardButton('Статистика', callback_data='owner_show_statistic')
kb_owner_manage_gives = InlineKeyboardMarkup().add(bt_owner_change_winners).add(bt_owner_statistic).add(
    bt_admin_cancel_action
)
