import asyncio

from data.config import (
    THROTTLING_SLEEP_TIME,
    CHAT_GPT_MESSAGE_KEY,
    VOICE_TYPE,
    TEXT_TYPE
)

from data.messages import THROTTLING_MESSAGE

from database import add_users_throttling_messages, add_users_messages, add_users_chat_gpt_messages

from loader import bot

from aiogram import types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware


class ThrottlingAndDatabaseMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.user_last_request = {}
        self.prefix = key_prefix
        super(ThrottlingAndDatabaseMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict) -> None:
        handler = current_handler.get()
        # Take the value of the attributes set by the rate_limit decoder from utils/misc/rate_limit.
        limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
        key = getattr(handler, 'throttling_key', f'{self.prefix}_{handler.__name__}')
        user_id = message.from_user.id
        # Throttling check.
        await self.throttling_check(user_id=user_id, limit=limit, key=key)
        # If the user has passed the throttling check then write his message to the database.
        if not self.user_last_request[user_id]['time_blocked']:
            message_type = TEXT_TYPE if message.voice is None else VOICE_TYPE

            if key == CHAT_GPT_MESSAGE_KEY:
                await add_users_chat_gpt_messages(user_id=user_id, message_type=message_type)
            else:
                await add_users_messages(user_id=user_id, message_type=message_type, message_key=key)

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict) -> None:
        handler = current_handler.get()
        # Take the value of the attributes set by the rate_limit decoder from utils/misc/rate_limit.
        limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
        key = getattr(handler, 'throttling_key', f'{self.prefix}_{handler.__name__}')
        user_id = callback.from_user.id
        # Throttling check.
        await self.throttling_check(user_id=user_id, limit=limit, key=key)

    @staticmethod
    async def get_current_time() -> int:
        loop = asyncio.get_running_loop()
        return int(loop.time())

    async def throttling_check(self, user_id: int, limit: int, key: str) -> None:
        '''
        :param user_id: Telegram user id.
        :param limit: The time that must pass between two messages of a user of the same key.
        :param key: Key for different types of messages. You can find them all in data/config/middlewares/config.
        :return: None.
        '''

        # Asynchronously get the current date in the format timestamp.
        now_time = await self.get_current_time()
        # Check user_id in the dictionary of storage user last request.
        if user_id in self.user_last_request:
            # If the user is blocked.
            if self.user_last_request[user_id]['time_blocked']:
                # Check if the blocking time has passed.
                if now_time - self.user_last_request[user_id]['time_blocked'] >= THROTTLING_SLEEP_TIME:
                    # Unlock the user by assigning time_blocked 0.
                    self.user_last_request[user_id]['time_blocked'] = 0
                    # Assign key time of its call.
                    self.user_last_request[user_id]['time_last_key_message'][key] = now_time
                else:
                    raise CancelHandler()
            else:
                # If the user has already sent a message with such a key.
                if key in self.user_last_request[user_id]['time_last_key_message']:
                    # If the user has exceeded the message limit for a certain key.
                    if now_time - self.user_last_request[user_id]['time_last_key_message'][key] < limit:
                        # For Chat GPT we will not output a violation message.
                        # because it is output at the beginning of working with Chat GPT.
                        if key != CHAT_GPT_MESSAGE_KEY:
                            await bot.send_message(
                                chat_id=user_id,
                                text=THROTTLING_MESSAGE.format(THROTTLING_SLEEP_TIME)
                            )
                        # Add the broken message to the database.
                        await add_users_throttling_messages(
                            user_id=user_id,
                            throttling_key=key,
                            sleep_time=THROTTLING_SLEEP_TIME
                        )
                        # Set the blocking time.
                        self.user_last_request[user_id]['time_blocked'] = now_time
                        raise CancelHandler()
                    else:
                        # Assign key time of its call.
                        self.user_last_request[user_id]['time_last_key_message'][key] = now_time
                else:
                    # Assign key time of its call.
                    self.user_last_request[user_id]['time_last_key_message'][key] = now_time
        else:
            # Add user_id in the dictionary of storage user last request.
            self.user_last_request[user_id] = {}
            # For each key the last time of its call is stored.
            self.user_last_request[user_id]['time_last_key_message'] = {key: now_time}
            # 0 - if user dont blocked else contains the blocking time.
            self.user_last_request[user_id]['time_blocked'] = 0
