from data.urls import ASU_TELEGRAM_NEWS_URL

from data.callbacks import (
    CALLBACK_DATA_GET_CALENDAR,
    CALLBACK_DATA_GET_WEEKLY_SCHEDULE,
    CALLBACK_DATA_GET_TOMORROW_SCHEDULE,
    CALLBACK_DATA_GET_ALLEGED_TARGET_SEPARATOR,
    CALLBACK_DATA_CONFIRM_CHAT_GPT_CLEAR_MESSAGES,
    CALLBACK_DATA_CANCEL_CHAT_GPT_CLEAR_MESSAGES,
    CALLBACK_DATA_CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU,
    CALLBACK_DATA_CANCEL_CHAT_GPT_CANCEL_TO_MAIN_MENU
)

from data.config import ROW_WIDTH

from data.messages import (
    FOLLOW_URL_IKB_MESSAGE,
    GET_CALENDAR_IKB_MESSAGE,
    GET_WEEKLY_SCHEDULE_IKB_MESSAGE,
    GET_TOMORROW_SCHEDULE_IKB_MESSAGE,
    CONFIRM_IKB_MESSAGE,
    CANCEL_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def clear_chat_gpt_messages_ikb() -> InlineKeyboardMarkup:
    '''
    :return: InlineKeyboardMarkup.
    '''

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(
        InlineKeyboardButton(
            text=CONFIRM_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_CONFIRM_CHAT_GPT_CLEAR_MESSAGES
        )
    )

    ikb.row(
        InlineKeyboardButton(
            text=CANCEL_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_CANCEL_CHAT_GPT_CLEAR_MESSAGES
        )
    )

    return ikb


def chat_gpt_return_to_main_menu_ikb() -> InlineKeyboardMarkup:
    '''
    :return: InlineKeyboardMarkup.
    '''

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(
        InlineKeyboardButton(
            text=CONFIRM_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU
        )
    )

    ikb.row(
        InlineKeyboardButton(
            text=CANCEL_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_CANCEL_CHAT_GPT_CANCEL_TO_MAIN_MENU
        )
    )

    return ikb


def get_asu_telegram_news_ikb() -> InlineKeyboardMarkup:
    '''
    :return: InlineKeyboardMarkup.
    '''

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.add(InlineKeyboardButton(text=FOLLOW_URL_IKB_MESSAGE, url=ASU_TELEGRAM_NEWS_URL))

    return ikb


def get_alleged_target_name_ikb(alleged_targets_dict: dict) -> InlineKeyboardMarkup:
    '''
    :param alleged_targets_dict: These are dict that store the name of the alleged target
        and an url to its weekly schedule.
    :return: InlineKeyboardMarkup.
    '''

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    for alleged_target in alleged_targets_dict.keys():
        ikb.add(InlineKeyboardButton(
            text=alleged_target,
            # Callback data looks like this: AT_alleged_target_name.
            # AT_ is CALLBACK_DATA_GET_ALLEGED_TARGET_SEPARATOR.
            # alleged_target_name is the name of the student or lecturer selected by the user.
            callback_data=f'{CALLBACK_DATA_GET_ALLEGED_TARGET_SEPARATOR}{alleged_target}')
        )

    return ikb


def get_today_schedule_ikb() -> InlineKeyboardMarkup:
    '''
    :return: InlineKeyboardMarkup.
    '''

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(
        InlineKeyboardButton(
            text=GET_TOMORROW_SCHEDULE_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_GET_TOMORROW_SCHEDULE
        )
    )

    ikb.row(
        InlineKeyboardButton(
            text=GET_WEEKLY_SCHEDULE_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_GET_WEEKLY_SCHEDULE
        )
    )

    ikb.row(
        InlineKeyboardButton(
            text=GET_CALENDAR_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_GET_CALENDAR
        )
    )

    return ikb


def get_tomorrow_schedule_ikb() -> InlineKeyboardMarkup:
    '''
    :return: InlineKeyboardMarkup.
    '''

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(
        InlineKeyboardButton(
            text=GET_WEEKLY_SCHEDULE_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_GET_WEEKLY_SCHEDULE
        )
    )

    ikb.row(
        InlineKeyboardButton(
            text=GET_CALENDAR_IKB_MESSAGE,
            callback_data=CALLBACK_DATA_GET_CALENDAR
        )
    )

    return ikb


def get_calendar_ikb() -> InlineKeyboardMarkup:
    '''
    :return: InlineKeyboardMarkup.
    '''

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(
            InlineKeyboardButton(
                text=GET_CALENDAR_IKB_MESSAGE,
                callback_data=CALLBACK_DATA_GET_CALENDAR
            )
    )

    return ikb
