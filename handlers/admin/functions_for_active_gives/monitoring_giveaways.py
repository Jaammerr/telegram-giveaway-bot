import asyncio
import datetime as datetime_

from datetime import datetime

from config import timezone_info
from aiogram import types

from app import dp
from database import GiveAway, TelegramChannel

from .handle_group_users import handle_new_users_in_groups
from .giveaway_end_notification import send_giveaway_end_notification
from .process_end_giveaway import process_end_of_giveaway


chat_ids = []


async def manage_active_giveaways():

    while True:
        giveaways = await GiveAway().all().filter(run_status=True).values(
            'type',
            'over_date',
            'callback_value',
            'captcha',
            'owner_id'
        )

        if giveaways:

            for giveaway in giveaways:

                if giveaway['type'] == 'comments':
                    channel_data = await TelegramChannel().filter(owner_id=giveaway['owner_id']).all().values(
                        'group_id'
                    )

                    for channel in channel_data:
                        if channel['group_id'] not in chat_ids:
                            chat_ids.append(channel['group_id'])

                            dp.register_message_handler(
                                handle_new_users_in_groups,
                                chat_id=channel['group_id'],
                                chat_type=types.ChatType.SUPERGROUP
                            )


                current_time = datetime.now(tz=timezone_info)


                if giveaway['type'] == 'button' and giveaway['captcha']:
                    hours_to_end = 3

                    time_diff = giveaway["over_date"] - current_time
                    if time_diff == datetime_.timedelta(hours=hours_to_end):
                        await send_giveaway_end_notification(
                            give_callback_value=giveaway['callback_value']
                        )

                if current_time >= giveaway["over_date"]:
                    await process_end_of_giveaway(
                        give_callback_value=giveaway['callback_value'],
                        owner_id=giveaway['owner_id']
                    )


        await asyncio.sleep(30)
