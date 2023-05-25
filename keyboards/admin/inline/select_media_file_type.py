from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action


bt_admin_add_media_video = InlineKeyboardButton('Видео', callback_data='admin_add_media_video')
bt_admin_add_media_photo = InlineKeyboardButton('Фото', callback_data='admin_add_media_photo')

kb_admin_select_media_file_type = InlineKeyboardMarkup().add(bt_admin_add_media_video, bt_admin_add_media_photo).add(bt_admin_cancel_action)


