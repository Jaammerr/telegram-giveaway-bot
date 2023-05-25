from aiogram import types
from aiogram.dispatcher import FSMContext

from app import bot, dp
from database import TelegramChannel
from keyboards import *
from states import CreatedGivesStates



@dp.callback_query_handler(
    text=bt_admin_add_group_for_channel.callback_data,
    state=CreatedGivesStates.show_connected_channel
)
async def add_new_group_for_channel(
        jam: types.CallbackQuery,
        state: FSMContext
):
    state_data = await state.get_data()

    bot_data = await bot.get_me()
    await jam.message.edit_text(
        f'1) Добавьте бота @{bot_data.username} в группу канала с правами: \n<code>- публикация сообщений\n- редактирование чужих сообщений</code>\n\n2) Перешлите репостом любое сообщение из группы: ',
        reply_markup=kb_admin_cancel_action
    )
    await CreatedGivesStates.add_group.set()





@dp.message_handler(
    state=CreatedGivesStates.add_group,
)
async def get_group_data(
    jam: types.Message,
    state: FSMContext
):
    try:

        group_data = jam.forward_from_chat

        if group_data.type == 'supergroup':

            member_info = await bot.get_chat_member(
                chat_id=group_data.id,
                user_id=bot.id
            )

            if member_info.status == 'administrator':
                state_data = await state.get_data()
                channel_callback_value = state_data['channel_callback_value']

                await TelegramChannel().filter(channel_callback_value=channel_callback_value).update(
                    group_id=group_data.id
                )

                await jam.answer(
                    '✅  <b>Группа успешно добавлена</b>',
                    reply_markup=kb_admin_manage_channels
                )
                await CreatedGivesStates.manage_channels.set()


        else:
            await jam.answer(
                '🚫  <b>Это не группа, попробуйте еще раз:</b> ',
                reply_markup=kb_admin_cancel_action
            )


    except Exception as error:
        await jam.answer(
            '🚫  <b>Ошибка! Проверьте права бота и перешлите репостом сообщение из группы еще раз:</b> ',
            reply_markup=kb_admin_cancel_action
        )
