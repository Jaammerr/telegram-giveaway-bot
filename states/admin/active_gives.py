from aiogram.dispatcher.filters.state import StatesGroup, State


class ActiveGivesStates(StatesGroup):
    select_give = State()
    manage_selected_give = State()
    show_statistic = State()
    stop_give = State()

