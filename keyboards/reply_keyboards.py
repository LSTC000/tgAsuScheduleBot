from data.config import RESIZE_KEYBOARD

from data.messages import ASU_TELEGRAM_NEWS_RKB_BUTTON_MESSAGE
from data.messages import ASU_HOUSING_LOCATION_RKB_BUTTON_MESSAGE
from data.messages import CLEAR_CHAT_GPT_MESSAGES_RKB_BUTTON_MESSAGE
from data.messages import CANCEL_TO_MAIN_MENU_RKB_BUTTON_MESSAGE
from data.messages import STUDENT_TARGET_RKB_BUTTON_MESSAGE
from data.messages import LECTURER_TARGET_RKB_BUTTON_MESSAGE
from data.messages import CHAT_GPT_MENU_RKB_BUTTON_MESSAGE
from data.messages import SCHEDULE_MENU_RKB_BUTTON_MESSAGE

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_rkb() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardMarkup(resize_keyboard=RESIZE_KEYBOARD)

    rkb.row(KeyboardButton(text=SCHEDULE_MENU_RKB_BUTTON_MESSAGE))
    rkb.row(KeyboardButton(text=CHAT_GPT_MENU_RKB_BUTTON_MESSAGE))

    rkb.add(
        KeyboardButton(text=ASU_HOUSING_LOCATION_RKB_BUTTON_MESSAGE),
        KeyboardButton(text=ASU_TELEGRAM_NEWS_RKB_BUTTON_MESSAGE)
    )

    return rkb


def get_schedule_menu_rkb() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardMarkup(resize_keyboard=RESIZE_KEYBOARD)

    rkb.row(KeyboardButton(text=STUDENT_TARGET_RKB_BUTTON_MESSAGE))
    rkb.row(KeyboardButton(text=LECTURER_TARGET_RKB_BUTTON_MESSAGE))
    rkb.row(KeyboardButton(text=CANCEL_TO_MAIN_MENU_RKB_BUTTON_MESSAGE))

    return rkb


def get_chat_gpt_menu_rkb() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardMarkup(resize_keyboard=RESIZE_KEYBOARD)

    rkb.row(KeyboardButton(text=CLEAR_CHAT_GPT_MESSAGES_RKB_BUTTON_MESSAGE))
    rkb.row(KeyboardButton(text=CANCEL_TO_MAIN_MENU_RKB_BUTTON_MESSAGE))

    return rkb
