from aiogram import types
from aiogram.dispatcher import FSMContext

from app import dp, bot
from database import GiveAway, GiveAwayStatistic
from utils import Captcha


captcha = Captcha()



async def manage_new_members_from_button_gives(
    jam: types.Message,
    give_callback_value: str,
    state: FSMContext
):


    if not await GiveAwayStatistic().exists_member(
        giveaway_callback_value=give_callback_value,
        member_username=jam.from_user.username
    ):

        give_data = await GiveAway().filter(callback_value=give_callback_value).all().values(
            'over_date',
            'captcha'
        )

        for give in give_data:

            if give['captcha']:
                await state.update_data(give_callback_value=give_callback_value)

                captcha.register_handlers(dp)
                await bot.send_message(
                    jam.from_user.id,
                    captcha.get_caption(),
                    reply_markup=captcha.get_captcha_keyboard()
                )


            else:
                await jam.answer(
                    '<b>Замечательно! Вы участвуете!</b>'
                )


                await GiveAwayStatistic().update_statistic_members(
                    giveaway_callback_value=give_callback_value,
                    new_member_username=jam.from_user.username,
                    new_member_id=jam.from_user.id
                )

    else:
        await jam.answer(
            '<b>Вы уже участвуете! Ожидайте итогов!</b>'
        )
