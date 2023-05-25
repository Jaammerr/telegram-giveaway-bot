from aiogram import types

from app import bot, dp
from states import CreatedGivesStates
from keyboards import *


@dp.callback_query_handler(
    text=bt_admin_manage_channels.callback_data,
    state=CreatedGivesStates.manage_selected_give,
)
async def process_manage_channels(jam: types.CallbackQuery):
    await jam.message.edit_text(
        'Выберите действие: ',
        reply_markup=kb_admin_manage_channels
    )
    await CreatedGivesStates.manage_channels.set()
