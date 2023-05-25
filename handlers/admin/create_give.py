import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities
from aiogram_calendar import dialog_cal_callback, DialogCalendar

from app import dp, bot
from keyboards import *
from states import CreateGiveStates
from .save_giveaway import save_giveaway
from database import GiveAway



@dp.callback_query_handler(
    text=bt_admin_create_give.callback_data,
    state='*'
)
async def start_create_give(jam: types.CallbackQuery):

    await jam.message.edit_text(
        'Выберите тип розыгрыша: ',
        reply_markup=kb_admin_select_type_of_give
    )



@dp.callback_query_handler(
    text=[
        bt_admin_give_type_button.callback_data,
        bt_admin_give_type_comments.callback_data
    ]
)
async def get_type_of_give(jam: types.CallbackQuery, state: FSMContext):
    callback = jam.data

    if callback == bt_admin_give_type_button.callback_data:
        await state.update_data(give_type='button')
    else:
        await state.update_data(give_type='comments')


    await jam.message.edit_text(
        'Введите название розыгрыша: ',
        reply_markup=kb_admin_cancel_action
    )
    await CreateGiveStates.get_name.set()




@dp.message_handler(state=CreateGiveStates.get_name)
async def get_give_name(jam: types.Message, state: FSMContext):
    give_name = jam.text

    if await GiveAway().exists_give_name(
        user_id=jam.from_user.id,
        name=give_name
    ):

        await jam.answer(
            'Розыгрыш с таким названием уже существует, попробуйте еще раз: ',
            reply_markup=kb_admin_cancel_action
        )


    else:
        await state.update_data(give_name=jam.text)

        await jam.answer(
            'Введите текст для розыгрыша: \n\n<code>Можно использовать HTML разметку</code>',
            reply_markup=kb_admin_cancel_action
        )
        await CreateGiveStates.get_text.set()



@dp.message_handler(state=CreateGiveStates.get_text)
async def get_give_text(jam: types.Message, state: FSMContext):
    give_text = jam.text

    try:
        await jam.answer(
            give_text,
            reply_markup=kb_admin_edit_give_text,
        )
        await state.update_data(give_text=give_text)

    except CantParseEntities:
        await jam.answer(
            'Ошибка в разметке текста, попробуйте еще раз: \n\n<code>Возможно вы забыли закрыть тег</code>',
            reply_markup=kb_admin_cancel_action
        )



@dp.callback_query_handler(
    text=[
        bt_admin_edit_give_text.callback_data,
        bt_admin_continue_create_give.callback_data
    ],
    state=CreateGiveStates.get_text
)
async def edit_give_text(jam: types.CallbackQuery, state: FSMContext):
    callback = jam.data

    if callback == bt_admin_edit_give_text.callback_data:
        await jam.message.edit_text(
            'Введите текст для розыгрыша: \n\n<code>Можно использовать HTML разметку</code>',
            reply_markup=kb_admin_cancel_action
        )
        await CreateGiveStates.get_text.set()

    else:

        await jam.message.edit_text(
            'Хотите добавить медиафайл для розыгрыша ?',
            reply_markup=kb_admin_add_give_photo
        )




@dp.callback_query_handler(
    text=[
        bt_admin_add_give_photo.callback_data,
        bt_admin_not_add_give_photo.callback_data
    ],
    state=CreateGiveStates.get_text
)
async def ask_about_media_files_for_give(jam: types.CallbackQuery, state: FSMContext):
    callback = jam.data

    if callback == bt_admin_add_give_photo.callback_data:
        await jam.message.edit_text(
            'Выберите тип медиафайла: ',
            reply_markup=kb_admin_select_media_file_type
        )
        await CreateGiveStates.get_type_of_media_file.set()

    else:
        await state.update_data(give_media_type=False)

        await jam.message.edit_text(
            "Выберите дату завершения розыгрыша: ",
            reply_markup=await DialogCalendar().start_calendar()
        )
        await CreateGiveStates.get_date.set()



@dp.callback_query_handler(
    text=[
        bt_admin_add_media_video.callback_data,
        bt_admin_add_media_photo.callback_data
    ],
    state=CreateGiveStates.get_type_of_media_file
)
async def get_type_of_media_file(
        jam: types.CallbackQuery,
        state: FSMContext
):
    callback = jam.data

    if callback == bt_admin_add_media_video.callback_data:
        await state.update_data(give_media_type='video')

        await jam.message.edit_text(
            'Отправьте видео для розыгрыша: ',
            reply_markup=kb_admin_cancel_action
        )

    else:
        await state.update_data(give_media_type='photo')

        await jam.message.edit_text(
            'Отправьте фото для розыгрыша: ',
            reply_markup=kb_admin_cancel_action
        )

    await CreateGiveStates.get_media_file.set()



@dp.message_handler(
    content_types=[
        'photo',
        'video',
        'animation'
    ],
    state=CreateGiveStates.get_media_file
)
async def download_give_photo(jam: types.Message, state: FSMContext):

    if jam.content_type == 'photo':
        file_id = jam.photo[-1].file_id

    else:
        file_id = jam[jam.content_type].file_id

    await state.update_data(give_media_id=file_id)

    await jam.answer(
        "Выберите дату завершения розыгрыша: ",
        reply_markup=await DialogCalendar().start_calendar()
    )
    await CreateGiveStates.get_date.set()


@dp.callback_query_handler(
    dialog_cal_callback.filter(),
    state=CreateGiveStates.get_date
)
async def get_over_date_give(jam: types.CallbackQuery, state: FSMContext, callback_data):
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
    state=CreateGiveStates.get_date
)
async def ask_about_edit_give_date(jam: types.CallbackQuery, state: FSMContext):
    callback = jam.data

    if callback == bt_admin_edit_give_date.callback_data:
        await jam.message.edit_text(
            "Выберите дату завершения розыгрыша: ",
            reply_markup=await DialogCalendar().start_calendar()
        )

    else:

        state_data = await state.get_data()
        if state_data['give_type'] == 'button':

            await jam.message.edit_text(
                'Хотите добавить капчу для розыгрыша ? (Защита от ботов)',
                reply_markup=kb_admin_add_captcha_for_give
            )
            await CreateGiveStates.get_answer_of_captcha.set()


        else:
            await state.update_data(give_captcha=False)

            await jam.message.edit_text(
                'Введите время завершения розыгрыша: \n\n<code>Например: 19:23</code>',
                reply_markup=kb_admin_cancel_action
            )
            await CreateGiveStates.get_time.set()


@dp.callback_query_handler(
    text=[
        bt_admin_add_captcha_for_give.callback_data,
        bt_admin_not_add_captcha_for_give.callback_data
    ],
    state=CreateGiveStates.get_answer_of_captcha
)
async def ask_about_captcha_for_give(jam: types.CallbackQuery, state: FSMContext):
    callback = jam.data

    if callback == bt_admin_add_captcha_for_give.callback_data:
        await state.update_data(give_captcha=True)
    else:
        await state.update_data(give_captcha=False)


    await jam.message.edit_text(
        'Введите время завершения розыгрыша: \n\n<code>Например: 19:23</code>',
        reply_markup=kb_admin_cancel_action
    )
    await CreateGiveStates.get_time.set()



@dp.message_handler(
    state=CreateGiveStates.get_time,
    regexp=re.compile(r'\d{2}:\d{2}')
)
async def get_over_time_for_give(jam: types.Message, state: FSMContext):
    hours, minutes = jam.text.split(':')

    if hours.isdigit() and int(hours) in range(0, 24) and minutes.isdigit() and int(minutes) in range(0, 60):
        await state.update_data(give_over_time=jam.text)

        await jam.answer(
            'Введите количество победителей: ',
            reply_markup=kb_admin_cancel_action
        )
        await CreateGiveStates.get_winners_count.set()

    else:
        await jam.answer(
            '🚫  Неверный формат времени, попробуйте еще раз: ',
        )




@dp.message_handler(
    state=CreateGiveStates.get_winners_count,
    regexp=re.compile(r'\d+')
)
async def get_count_winners_for_give(jam: types.Message, state: FSMContext):
    await state.update_data(give_winners_count=int(jam.text))

    await save_giveaway(
        user_id=jam.from_user.id,
        state=state,
    )

    await bot.send_message(
        chat_id=jam.from_user.id,
        text='✅  <b>Розыгрыш успешно создан</b>',
        reply_markup=kb_admin_menu
    )

    await state.finish()
