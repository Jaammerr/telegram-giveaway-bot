from database import GiveAway, TelegramChannel
from app import bot




async def check_channels_subscriptions(
        give_callback_value: str,
        user_id: int,
        owner_id: int = False
) -> bool:

    if not owner_id:

        owner_id = await GiveAway().get_owner_by_callback_value(
            give_callback_value=give_callback_value
        )


    channels_data = await TelegramChannel().get_channel_data(
        owner_id=owner_id
    )

    for channel in channels_data:

        channel_id = channel['channel_id']
        user_channel_info = await bot.get_chat_member(
            chat_id=channel_id,
            user_id=user_id
        )

        if user_channel_info['status'] == 'member':
            continue

        else:
            return False

    else:
        return True




