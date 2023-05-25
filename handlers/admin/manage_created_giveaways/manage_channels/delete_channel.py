from aiogram import types
from aiogram.dispatcher import FSMContext

from app import dp
from database import TelegramChannel
from states import CreatedGivesStates
from keyboards import *



@dp.callback_query_handler(
    text=bt_admin_delete_channel.callback_data,
    state=CreatedGivesStates.show_connected_channel
)
async def delete_channel(
    jam: types.CallbackQuery,
    state: FSMContext
):
    state_data = await state.get_data()

    await TelegramChannel().delete_channel(
        channel_callback_value=state_data['channel_callback_value']
    )

    await jam.message.edit_text(
        '✅  <b>Канал успешно удален</b>',
        reply_markup=kb_admin_manage_channels
    )

    await CreatedGivesStates.manage_channels.set()
