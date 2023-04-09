from data.config import CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE
from data.config import RATE_LIMIT_DICT
from data.config import MENU_REPLAY_KEYBOARD_KEY

from data.messages import CHOICE_SCHEDULE_TARGET_MESSAGE
from data.messages import ENTER_CHAT_GPT_QUESTION_MESSAGE
from data.messages import ASU_BUILDINGS_LOCATION_MESSAGE
from data.messages import SCHEDULE_MENU_RKB_BUTTON_MESSAGE
from data.messages import CHAT_GPT_MENU_RKB_BUTTON_MESSAGE
from data.messages import ASU_TELEGRAM_NEWS_RKB_BUTTON_MESSAGE
from data.messages import ASU_HOUSING_LOCATION_RKB_BUTTON_MESSAGE

from keyboards import get_schedule_menu_rkb
from keyboards import get_asu_telegram_news_ikb
from keyboards import get_chat_gpt_menu_rkb

from utils import rate_limit

from loader import dp, bot
from states import MenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(
    lambda m: m.text in [
        SCHEDULE_MENU_RKB_BUTTON_MESSAGE,
        CHAT_GPT_MENU_RKB_BUTTON_MESSAGE,
        ASU_TELEGRAM_NEWS_RKB_BUTTON_MESSAGE,
        ASU_HOUSING_LOCATION_RKB_BUTTON_MESSAGE
    ],
    content_types=types.ContentType.TEXT,
    state=MenuStatesGroup.main_menu
)
@rate_limit(limit=RATE_LIMIT_DICT[MENU_REPLAY_KEYBOARD_KEY], key=MENU_REPLAY_KEYBOARD_KEY)
async def main_menu(message: types.Message, state: FSMContext) -> None:
    text = message.text
    # Perform an action depending on the button pressed by the user in the main menu
    if text == SCHEDULE_MENU_RKB_BUTTON_MESSAGE:
        msg = CHOICE_SCHEDULE_TARGET_MESSAGE
        kb = get_schedule_menu_rkb()

        await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=kb)
        await MenuStatesGroup.schedule_menu.set()
    elif text == CHAT_GPT_MENU_RKB_BUTTON_MESSAGE:
        msg = ENTER_CHAT_GPT_QUESTION_MESSAGE
        kb = get_chat_gpt_menu_rkb()
        # Create variables in the user memory storage
        async with state.proxy() as data:
            data['chat_gpt_messages'] = [CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE]
            data['count_chat_gpt_messages'] = 0

        await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=kb)
        await MenuStatesGroup.chat_gpt_menu.set()
    elif text == ASU_TELEGRAM_NEWS_RKB_BUTTON_MESSAGE:
        msg = ASU_TELEGRAM_NEWS_RKB_BUTTON_MESSAGE
        kb = get_asu_telegram_news_ikb()
        await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=kb)
    else:
        msg = ASU_BUILDINGS_LOCATION_MESSAGE
        await bot.send_message(chat_id=message.from_user.id, text=msg)
