from aiogram import types
from aiogram.dispatcher import FSMContext

from app import dp
from keyboards import *
from database import GiveAway, TelegramChannel, GiveAwayStatistic
from states import CreatedGivesStates



@dp.callback_query_handler(
    text=bt_admin_delete_give.callback_data,
    state=CreatedGivesStates.manage_selected_give,
)
async def delete_give(
    jam: types.CallbackQuery,
    state: FSMContext
):
    state_data = await state.get_data()
    give_callback_value = state_data.get('give_callback_value')

    await GiveAway().delete_give(
        callback_value=give_callback_value
    )

    await TelegramChannel().delete_channel(
        give_callback_value=give_callback_value
    )

    await GiveAwayStatistic().delete_statistic(
        giveaway_callback_value=give_callback_value
    )


    await jam.message.edit_text(
        '✅  <b>Розыгрыш успешно удален</b>',
        reply_markup=kb_admin_menu
    )
    await state.finish()