__all__ = ['register_users_cancels']


from .cancel_from_schedule_menu import cancel_to_main_menu_from_schedule_menu
from .cancel_from_chat_gpt_menu import cancel_to_main_menu_from_chat_gpt_menu, confirm_chat_gpt_cancel_to_main_menu

from aiogram import Dispatcher


def register_users_cancels(dp: Dispatcher):
    dp.register_message_handler(cancel_to_main_menu_from_schedule_menu)
    dp.register_message_handler(cancel_to_main_menu_from_chat_gpt_menu)
    dp.register_callback_query_handler(confirm_chat_gpt_cancel_to_main_menu)
