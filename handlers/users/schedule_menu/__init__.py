__all__ = ['register_users_schedule_menu']


from .first_choice_schedule_target import first_choice_schedule_target
from .swap_schedule_target import swap_schedule_target
from .get_today_schedule import get_today_schedule
from .choice_alleged_target_name import choice_alleged_target_name
from .get_tomorrow_schedule import get_tomorrow_schedule
from .get_weekly_schedule import get_weekly_schedule
from .get_calendar_schedule import get_calendar
from .get_calendar_schedule import get_calendar_schedule

from aiogram import Dispatcher


def register_users_schedule_menu(dp: Dispatcher):
    dp.register_message_handler(first_choice_schedule_target)
    dp.register_message_handler(swap_schedule_target)
    dp.register_message_handler(get_today_schedule)
    dp.register_callback_query_handler(choice_alleged_target_name)
    dp.register_callback_query_handler(get_tomorrow_schedule)
    dp.register_callback_query_handler(get_weekly_schedule)
    dp.register_callback_query_handler(get_calendar)
    dp.register_callback_query_handler(get_calendar_schedule)
