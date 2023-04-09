__all__ = ['register_users_chat_gpt_menu']


from .clear_chat_gpt_messages import clear_chat_gpt_messages
from .clear_chat_gpt_messages import confirm_clear_chat_gpt_messages
from .chat_gpt_response import chat_gpt_response

from aiogram import Dispatcher


def register_users_chat_gpt_menu(dp: Dispatcher):
    dp.register_message_handler(clear_chat_gpt_messages)
    dp.register_callback_query_handler(confirm_clear_chat_gpt_messages)
    dp.register_message_handler(chat_gpt_response)
