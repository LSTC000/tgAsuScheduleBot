__all__ = ['register_users_commands', 'set_default_commands']


from .start import start_command
from .help import help_command
from .setting_commands import set_default_commands

from aiogram import Dispatcher


def register_users_commands(dp: Dispatcher):
    dp.register_message_handler(start_command)
    dp.register_message_handler(help_command)
