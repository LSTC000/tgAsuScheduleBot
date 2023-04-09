__all__ = [
    'chat_gpt_clear_history_message_ikb',
    'chat_gpt_return_to_main_menu_ikb',
    'get_asu_telegram_news_ikb',
    'get_alleged_target_name_ikb',
    'get_today_schedule_ikb',
    'get_tomorrow_schedule_ikb',
    'get_main_menu_rkb',
    'get_schedule_menu_rkb',
    'get_chat_gpt_menu_rkb',
    'get_calendar_ikb'
]


from .inline_keyboards import (
    chat_gpt_clear_history_message_ikb,
    chat_gpt_return_to_main_menu_ikb,
    get_asu_telegram_news_ikb,
    get_alleged_target_name_ikb,
    get_today_schedule_ikb,
    get_tomorrow_schedule_ikb,
    get_calendar_ikb
)

from .reply_keyboards import (
    get_main_menu_rkb,
    get_schedule_menu_rkb,
    get_chat_gpt_menu_rkb
)
