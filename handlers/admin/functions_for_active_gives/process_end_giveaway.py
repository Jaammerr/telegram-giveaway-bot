from database import GiveAway, TelegramChannel, GiveAwayStatistic
from .winners_animation import run_winners_animation



async def process_end_of_giveaway(
        give_callback_value: str,
        owner_id: int
):
    winners_data = await GiveAway().filter(callback_value=give_callback_value).all().values('winners_count')
    channels_data = await TelegramChannel().get_channel_data(owner_id=owner_id)
    statistic_data = await GiveAwayStatistic().filter(giveaway_callback_value=give_callback_value).all().values(
        'members',
        'winners'
    )


    for winners in winners_data:
        for statistic in statistic_data:
            for channel in channels_data:


                await run_winners_animation(
                    give_callback_value=give_callback_value,
                    channel_id=channel['channel_id'],
                    members_from_giveaway=statistic['members'],
                    winners_count=winners['winners_count'],
                    winners_users=statistic['winners'] if statistic['winners'] else []
                )
