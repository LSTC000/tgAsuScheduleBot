from data.config import RATE_LIMIT_DICT
from data.config import COMMAND_KEY

from data.messages import HELP_COMMAND_MESSAGE

from loader import dp, bot

from utils import rate_limit

from aiogram import types


@dp.message_handler(commands=['help'], state='*')
@rate_limit(limit=RATE_LIMIT_DICT[COMMAND_KEY], key=COMMAND_KEY)
async def help_command(message: types.Message) -> None:
    msg = HELP_COMMAND_MESSAGE.format(message.from_user.first_name)
    await bot.send_message(chat_id=message.from_user.id, text=msg)
