__all__ = ['register_users_text_out_of_state']


from .invalid_restart_bot_message import invalid_restart_bot_message
from .invalid_main_menu_message import invalid_main_menu_message
from .invalid_schedule_menu_message import invalid_schedule_menu_message
from .invalid_chat_gpt_clear_messages_message import invalid_chat_gpt_clear_messages_message
from .invalid_chat_gpt_cancel_to_main_menu_message import invalid_chat_gpt_cancel_to_main_menu_message

from aiogram import Dispatcher


def register_users_text_out_of_state(dp: Dispatcher):
    dp.register_message_handler(invalid_restart_bot_message)
    dp.register_message_handler(invalid_main_menu_message)
    dp.register_message_handler(invalid_schedule_menu_message)
    dp.register_message_handler(invalid_chat_gpt_clear_messages_message)
    dp.register_message_handler(invalid_chat_gpt_cancel_to_main_menu_message)
