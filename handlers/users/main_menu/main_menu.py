from data.redis import COUNT_CHAT_GPT_MESSAGES_KEY, CHAT_GPT_MESSAGES_KEY

from data.config import CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE, RATE_LIMIT_DICT, MENU_REPLAY_KEYBOARD_KEY

from data.messages import (
    CHOICE_SCHEDULE_TARGET_MESSAGE,
    ENTER_CHAT_GPT_QUESTION_MESSAGE,
    ASU_BUILDINGS_LOCATION_MESSAGE,
    SCHEDULE_MENU_RKB_MESSAGE,
    CHAT_GPT_MENU_RKB_MESSAGE,
    ASU_TELEGRAM_NEWS_RKB_MESSAGE,
    ASU_HOUSING_LOCATION_RKB_MESSAGE
)

from keyboards import get_schedule_menu_rkb, get_asu_telegram_news_ikb, get_chat_gpt_menu_rkb

from utils import rate_limit

from loader import dp, bot

from states import MenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(
    lambda m: m.text in [
        SCHEDULE_MENU_RKB_MESSAGE,
        CHAT_GPT_MENU_RKB_MESSAGE,
        ASU_TELEGRAM_NEWS_RKB_MESSAGE,
        ASU_HOUSING_LOCATION_RKB_MESSAGE
    ],
    content_types=types.ContentType.TEXT,
    state=MenuStatesGroup.main_menu
)
@rate_limit(limit=RATE_LIMIT_DICT[MENU_REPLAY_KEYBOARD_KEY], key=MENU_REPLAY_KEYBOARD_KEY)
async def main_menu(message: types.Message, state: FSMContext) -> None:
    text = message.text
    # Perform an action depending on the button pressed by the user in the main menu.
    if text == SCHEDULE_MENU_RKB_MESSAGE:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=CHOICE_SCHEDULE_TARGET_MESSAGE,
            reply_markup=get_schedule_menu_rkb()
        )
        await MenuStatesGroup.schedule_menu.set()
    elif text == CHAT_GPT_MENU_RKB_MESSAGE:
        # Create variables in the user memory storage.
        async with state.proxy() as data:
            data[CHAT_GPT_MESSAGES_KEY] = [CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE]
            data[COUNT_CHAT_GPT_MESSAGES_KEY] = 0

        await bot.send_message(
            chat_id=message.from_user.id,
            text=ENTER_CHAT_GPT_QUESTION_MESSAGE,
            reply_markup=get_chat_gpt_menu_rkb()
        )
        await MenuStatesGroup.chat_gpt_menu.set()
    elif text == ASU_TELEGRAM_NEWS_RKB_MESSAGE:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=ASU_TELEGRAM_NEWS_RKB_MESSAGE,
            reply_markup=get_asu_telegram_news_ikb()
        )
    else:
        await bot.send_message(chat_id=message.from_user.id, text=ASU_BUILDINGS_LOCATION_MESSAGE)
