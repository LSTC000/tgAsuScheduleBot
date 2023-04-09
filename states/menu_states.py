from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuStatesGroup(StatesGroup):
    main_menu = State()
    schedule_menu = State()
    chat_gpt_menu = State()
