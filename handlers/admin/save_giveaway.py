import datetime

from aiogram.dispatcher import FSMContext
from database import GiveAway




async def save_giveaway(user_id: int, state: FSMContext):
    state_data = await state.get_data()

    give_type = state_data.get('give_type')
    give_name = state_data.get('give_name')
    give_text = state_data.get('give_text')
    give_media_type = state_data.get('give_media_type')
    give_date = state_data.get('give_over_date')
    give_time = state_data.get('give_over_time')
    give_captcha = state_data.get('give_captcha')
    give_winners_count = state_data.get('give_winners_count')

    over_date = datetime.datetime(
        year=give_date.year,
        month=give_date.month,
        day=give_date.day,
        hour=int(give_time.split(':')[0]),
        minute=int(give_time.split(':')[1]),
    )

    await GiveAway().create_give(
        owner_id=user_id,
        name=give_name,
        type_of_give=give_type,
        text=give_text,
        photo_id=state_data['give_media_id'] if give_media_type == 'photo' else None,
        video_id=state_data['give_media_id'] if give_media_type == 'video' else None,
        over_date=over_date,
        captcha=give_captcha,
        winners_count=give_winners_count
    )
