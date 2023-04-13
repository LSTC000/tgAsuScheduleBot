from data.config import RATE_LIMIT_DICT, INVALID_MESSAGE_KEY

from data.messages import INVALID_SCHEDULE_MENU_MESSAGE

from utils import rate_limit

from loader import dp, bot

from states import MenuStatesGroup

from aiogram import types


@dp.message_handler(content_types=types.ContentType.TEXT, state=MenuStatesGroup.schedule_menu)
@rate_limit(limit=RATE_LIMIT_DICT[INVALID_MESSAGE_KEY], key=INVALID_MESSAGE_KEY)
async def invalid_schedule_menu_message(message: types.Message) -> None:
    await bot.send_message(
        chat_id=message.from_user.id,
        text=INVALID_SCHEDULE_MENU_MESSAGE.format(message.from_user.first_name)
    )
