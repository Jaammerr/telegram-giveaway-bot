from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateGiveStates(StatesGroup):
    get_name = State()
    get_text = State()
    get_media_file = State()
    get_date = State()
    get_time = State()
    get_type_of_media_file = State()
    get_answer_of_captcha = State()
    get_winners_count = State()
