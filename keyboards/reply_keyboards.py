from data.config import RESIZE_KEYBOARD

from data.messages import (
    ASU_TELEGRAM_NEWS_RKB_MESSAGE,
    ASU_BUILDINGS_LOCATION_RKB_MESSAGE,
    CLEAR_CHAT_GPT_MESSAGES_RKB_MESSAGE,
    CANCEL_TO_MAIN_MENU_RKB_MESSAGE,
    STUDENT_TARGET_RKB_MESSAGE,
    LECTURER_TARGET_RKB_MESSAGE,
    CHAT_GPT_MENU_RKB_MESSAGE,
    SCHEDULE_MENU_RKB_MESSAGE
)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_rkb() -> ReplyKeyboardMarkup:
    '''
    :return: ReplyKeyboardMarkup.
    '''

    rkb = ReplyKeyboardMarkup(resize_keyboard=RESIZE_KEYBOARD)

    rkb.row(KeyboardButton(text=SCHEDULE_MENU_RKB_MESSAGE))
    rkb.row(KeyboardButton(text=CHAT_GPT_MENU_RKB_MESSAGE))

    rkb.add(
        KeyboardButton(text=ASU_BUILDINGS_LOCATION_RKB_MESSAGE),
        KeyboardButton(text=ASU_TELEGRAM_NEWS_RKB_MESSAGE)
    )

    return rkb


def get_schedule_menu_rkb() -> ReplyKeyboardMarkup:
    '''
    :return: ReplyKeyboardMarkup.
    '''

    rkb = ReplyKeyboardMarkup(resize_keyboard=RESIZE_KEYBOARD)

    rkb.row(KeyboardButton(text=STUDENT_TARGET_RKB_MESSAGE))
    rkb.row(KeyboardButton(text=LECTURER_TARGET_RKB_MESSAGE))
    rkb.row(KeyboardButton(text=CANCEL_TO_MAIN_MENU_RKB_MESSAGE))

    return rkb


def get_chat_gpt_menu_rkb() -> ReplyKeyboardMarkup:
    '''
    :return: ReplyKeyboardMarkup.
    '''

    rkb = ReplyKeyboardMarkup(resize_keyboard=RESIZE_KEYBOARD)

    rkb.row(KeyboardButton(text=CLEAR_CHAT_GPT_MESSAGES_RKB_MESSAGE))
    rkb.row(KeyboardButton(text=CANCEL_TO_MAIN_MENU_RKB_MESSAGE))

    return rkb
