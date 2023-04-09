from aiogram.dispatcher.filters.state import StatesGroup, State


class ChatGptMenuStatesGroup(StatesGroup):
    chat_gpt_clear_messages = State()
    chat_gpt_confirm_cancel_to_main_menu = State()
