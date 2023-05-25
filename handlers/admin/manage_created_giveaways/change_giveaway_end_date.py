import datetime
import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram_calendar import DialogCalendar, dialog_cal_callback
from app import dp
from keyboards import *
from database import GiveAway
from states import CreatedGivesStates






@dp.callback_query_handler(
    text=bt_admin_change_over_date.callback_data,
    state=CreatedGivesStates.manage_selected_give,
)
async def change_over_date_of_give(
    jam: types.CallbackQuery,
    state: FSMContext
):
    await CreatedGivesStates.change_over_date.set()

    await jam.message.edit_text(
        "Выберите дату завершения розыгрыша: ",
        reply_markup=await DialogCalendar().start_calendar()
    )




@dp.callback_query_handler(
    dialog_cal_callback.filter(),
    state=CreatedGivesStates.change_over_date
)
async def get_changed_over_date_of_give(
    jam: types.CallbackQuery,
    state: FSMContext,
    callback_data
):
    selected, date = await DialogCalendar().process_selection(jam, callback_data)

    if selected:
        await state.update_data(give_over_date=date)
        await jam.message.edit_text(
            f'Выбранная дата: {date.strftime("%d/%m/%Y")}',
            reply_markup=kb_admin_edit_give_date
        )




@dp.callback_query_handler(
    text=[
        bt_admin_edit_give_date.callback_data,
        bt_admin_continue_create_give.callback_data
    ],
    state=CreatedGivesStates.change_over_date,
)
async def edit_created_give_over_date(
    jam: types.CallbackQuery,
    state: FSMContext
):
    callback = jam.data

    if callback == bt_admin_edit_give_date.callback_data:
        await jam.message.edit_text(
            "Выберите дату завершения розыгрыша: ",
            reply_markup=await DialogCalendar().start_calendar()
        )

    else:
        await jam.message.edit_text(
            'Введите время завершения розыгрыша: \n\n<code>Например: 19:23</code>',
            reply_markup=kb_admin_cancel_action
        )
        await CreatedGivesStates.change_time.set()



@dp.message_handler(
    state=CreatedGivesStates.change_time,
    regexp=re.compile(r'\d{2}:\d{2}')
)
async def get_over_time_for_give(
    jam: types.Message,
    state: FSMContext
):
    give_time = jam.text

    state_data = await state.get_data()
    give_callback_value = state_data.get('give_callback_value')
    give_date = state_data.get('give_over_date')


    over_date = datetime.datetime(
        year=give_date.year,
        month=give_date.month,
        day=give_date.day,
        hour=int(give_time.split(':')[0]),
        minute=int(give_time.split(':')[1]),
    )



    await GiveAway().change_give_over_date(
        callback_value=give_callback_value,
        over_date=over_date
    )


    await jam.answer(
        '✅  <b>Дата окончания успешно изменена</b>',
        reply_markup=kb_admin_menu
    )
