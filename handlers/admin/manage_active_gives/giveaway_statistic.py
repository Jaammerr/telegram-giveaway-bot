from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp
from database import GiveAwayStatistic
from keyboards import *
from states import ActiveGivesStates




@dp.callback_query_handler(
    text=bt_admin_show_statistic.callback_data,
    state=ActiveGivesStates.manage_selected_give
)
async def show_give_statistic(
    jam: types.CallbackQuery,
    state: FSMContext
):
    await ActiveGivesStates.show_statistic.set()
    state_data = await state.get_data()

    statistic_info = await GiveAwayStatistic().get_statistic(
        giveaway_callback_value=state_data['give_callback_value']
    )

    if statistic_info:
        await jam.message.edit_text(
            f'➖  <b>Количество участников за последние 24 часа:</b> {statistic_info.count_members_in_24_hours}\n➖  <b>Общее количество участников:</b> {statistic_info.count_members_summary}',
            reply_markup=kb_admin_cancel_action
        )

    else:
        await jam.answer('В розыгрыше нет участников')
