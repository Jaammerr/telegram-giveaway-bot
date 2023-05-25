from aiogram.dispatcher.filters.state import StatesGroup, State


class CreatedGivesStates(StatesGroup):
    select_give = State()
    manage_selected_give = State()
    manage_channels = State()
    add_channel = State()
    add_group = State()
    select_connected_channel = State()
    show_connected_channel = State()
    change_over_date = State()
    change_time = State()
