import asyncio
import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified

from app import bot
from database import TemporaryUsers, GiveAwayStatistic

from .inform_of_the_end_give import delete_and_inform_of_the_end_give



async def create_markup_for_watch_results(
        give_callback_value: str
) -> InlineKeyboardMarkup:

    bot_data = await bot.get_me()
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text='Присоединиться »',
            url=f'https://t.me/{bot_data.username}?start={give_callback_value}=watchresult'
        )
    )

    return markup



async def create_markup_for_watch_winners(
        give_callback_value: str
) -> InlineKeyboardMarkup:

    bot_data = await bot.get_me()
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text='Результаты »',
            url=f'https://t.me/{bot_data.username}?start={give_callback_value}=getresults'
        )
    )

    return markup



async def run_winners_animation(
    give_callback_value: str,
    channel_id: int,
    members_from_giveaway: list,
    winners_count: int,
    winners_users: list = False
):

    """members_from_giveaway = [{'user_id': int(f'34534{i}')} for i in range(100)]
    temporary_users_usernames = []


    for i, member_info in enumerate(members_from_giveaway):
        temporary_users_usernames.append(user{i + 1}')

        member_info.update({
            'place': i + 1,
            'username': user{i + 1}'
        })"""


    summary_members_count = len(members_from_giveaway)
    if len(members_from_giveaway) >= winners_count:

        markup = await create_markup_for_watch_results(give_callback_value)
        await bot.send_message(
            chat_id=channel_id,
            text=f'<b>💎  Начало выбора победителя через 10 минут</b>',
            reply_markup=markup
        )
        await asyncio.sleep(20)


        if winners_users:
            if len(winners_users) < winners_count:

                for place_number in range(1, winners_count+1):

                    for winner_info in winners_users:
                        if winner_info['place'] != place_number:

                            member_info = random.choice(members_from_giveaway)
                            winners_users.append(
                                {
                                    'place': place_number,
                                    'user_id': member_info['user_id'],
                                    'username': member_info['username']
                                }
                            )

                            members_from_giveaway.remove(member_info)

                        else:
                            continue

        else:

            for place_number in range(1, winners_count+1):

                member_info = random.choice(members_from_giveaway)

                for winner_info in winners_users:
                    if winner_info['user_id'] == member_info['user_id']:
                        continue

                    else:
                        winners_users.append(
                            {
                                'place': place_number,
                                'user_id': member_info['user_id'],
                                'username': member_info['username']
                            }
                        )

                else:
                    winners_users.append(
                        {
                            'place': place_number,
                            'user_id': member_info['user_id'],
                            'username': member_info['username']
                        }
                    )

                members_from_giveaway.remove(member_info)


        temporary_users_for_watch_results = await TemporaryUsers().get_all_users(
            callback_value=give_callback_value
        )

        if temporary_users_for_watch_results:
            users_to_send_messages = []

            for user in temporary_users_for_watch_results:

                message = await bot.send_message(
                    chat_id=user['user_id'],
                    text='💎  <b>Начинается выбор победителя</b>'
                )

                users_to_send_messages.append(
                    {
                        'user_id': user['user_id'],
                        'message_id': message.message_id
                    }
                )


            members_usernames = []
            for member_info in members_from_giveaway:
                members_usernames.append(member_info['username'])


            while len(members_usernames) > 1:

                username = ''
                text = ''

                try:
                    chunks = [
                        members_usernames[i:i + 12]
                        for i in range(0, len(members_usernames), 8)
                    ]

                    for chunk in chunks:

                        index = random.randint(0, len(chunk) - 1)
                        username = chunk[index]

                        chunk.pop(index)
                        members_usernames.remove(username)

                        users_formatted = [f'🎁 {user}  ' for user in chunk]
                        text = ''

                        for i, user in enumerate(users_formatted):
                            if i % 4 == 0 and i > 0:
                                text += '\n'

                            text += user + ' '

                    for user_to_send in users_to_send_messages:
                        try:
                            await bot.edit_message_text(
                                chat_id=user_to_send['user_id'],
                                message_id=user_to_send['message_id'],
                                text=f'🔫  <b>Выбывает: {username}</b>\n\n<b>{text}</b>'
                            )
                        except MessageNotModified:
                            continue

                    await asyncio.sleep(0.3)

                except ValueError:
                    continue

            else:
                text = ""
                for i in range(len(winners_users)):
                    user_info = winners_users[i]
                    text += f"{user_info['place']} место - @{user_info['username']}"
                    if i < len(winners_users) - 1:
                        text += "\n"


                for user_to_send in users_to_send_messages:
                    await bot.edit_message_text(
                        chat_id=user_to_send['user_id'],
                        message_id=user_to_send['message_id'],
                        text=text
                    )


        await GiveAwayStatistic().filter(
            giveaway_callback_value=give_callback_value
        ).update(
            winners=winners_users
        )


        markup = await create_markup_for_watch_winners(give_callback_value)
        await bot.send_message(
            chat_id=channel_id,
            text=f'<b>Розыгрыш завершен ✅</b>',
            reply_markup=markup
        )



    else:
        await bot.send_message(
            chat_id=channel_id,
            text=f'<b>🚫  Розыгрыш завершен, победителей выбрать не удалось, участников слишком мало</b>',
        )


    await delete_and_inform_of_the_end_give(
        give_callback_value=give_callback_value,
        winners=winners_users,
        summary_count_users=summary_members_count
    )
