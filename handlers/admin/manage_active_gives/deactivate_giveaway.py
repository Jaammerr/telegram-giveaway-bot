from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp
from database import GiveAway, GiveAwayStatistic
from keyboards import *
from states import ActiveGivesStates



@dp.callback_query_handler(
    text=bt_admin_stop_give.callback_data,
    state=ActiveGivesStates.manage_selected_give
)
async def stop_give(jam: types.CallbackQuery, state: FSMContext):
    await ActiveGivesStates.stop_give.set()
    state_data = await state.get_data()

    await GiveAway().update_give_status(
        callback_value=state_data['give_callback_value'],
        status=False
    )

    await GiveAwayStatistic().filter(
        giveaway_callback_value=state_data['give_callback_value']
    ).delete()

    await jam.message.edit_text(
        '✅  <b>Розыгрыш остановлен</b>',
        reply_markup=kb_admin_menu
    )
    await state.finish()