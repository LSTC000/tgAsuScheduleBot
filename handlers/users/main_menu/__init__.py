__all__ = ['register_users_main_menu']


from .main_menu import main_menu

from aiogram import Dispatcher


def register_users_main_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu)
