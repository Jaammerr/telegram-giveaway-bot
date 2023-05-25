from app import bot
from database import GiveAway, TelegramChannel, TemporaryUsers


async def delete_and_inform_of_the_end_give(
    give_callback_value: str,
    winners: list,
    summary_count_users: int,
):
    give_data = await GiveAway().filter(callback_value=give_callback_value).all().values(
        'owner_id',
        'name'
    )



    for give in give_data:

        if summary_count_users >= len(winners):

            text = f'🎁  <b>Розыгрыш завершен</b>\n\n<b>Название:</b> {give["name"]}\n<b>Общее количество участников:</b> {summary_count_users}\n\n<b>Победители:</b>\n\n'
            for i in range(len(winners)):
                user_info = winners[i]
                text += f"{user_info['place']} место - @{user_info['username']}"
                if i < len(winners) - 1:
                    text += "\n"


            await bot.send_message(
                chat_id=give['owner_id'],
                text=text
            )

        else:
            await bot.send_message(
                chat_id=give['owner_id'],
                text=f'🎁  <b>Розыгрыш завершен</b>\n\n<b>Название:</b> {give["name"]}\n<b>Победителей выбрать не удалось, участников слишком мало</b>'
            )


    await GiveAway().delete_give(callback_value=give_callback_value)
    await TemporaryUsers().filter(giveaway_callback_value=give_callback_value).delete()
