from aiogram import types
from aiogram.dispatcher import FSMContext

from app import dp
from database import TelegramChannel
from states import CreatedGivesStates
from keyboards import *



@dp.callback_query_handler(
    lambda c: c.data != bt_admin_cancel_action.callback_data,
    state=CreatedGivesStates.select_connected_channel,
)
async def show_selected_channel(
    jam: types.CallbackQuery,
    state: FSMContext
):
    channel_callback_value = jam.data
    await state.update_data(channel_callback_value=channel_callback_value)

    channel_data = await TelegramChannel().get_channel_data(
        channel_callback_value=channel_callback_value
    )

    for channel in channel_data:
        await jam.message.edit_text(
            f'<b>ID канала:</b> <code>{channel["channel_id"]}</code>\n<b>ID группы:</b> <code>{channel["group_id"] if channel["group_id"] else "не подключена"}\n</code>\n<b>Название канала:</b> <code>{channel["name"]}</code>',
            reply_markup=kb_admin_manage_selected_channel
        )

    await CreatedGivesStates.show_connected_channel.set()
