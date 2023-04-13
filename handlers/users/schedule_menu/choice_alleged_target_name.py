from data.callbacks import CALLBACK_DATA_GET_ALLEGED_TARGET_SEPARATOR

from data.memory_storage import (
    TARGET_URL_KEY,
    ALLEGED_TARGET_NAME_KEY,
    ALLEGED_TARGET_INFO_KEY,
    SCHEDULE_INLINE_KEYBOARDS_KEY
)

from data.config import RATE_LIMIT_DICT, SCHEDULE_INLINE_KEYBOARD_KEY

from data.messages import CALLBACK_DATA_KEY_ERROR_MESSAGE

from functions import get_daily_schedule

from utils import rate_limit

from loader import dp, bot

from states import ScheduleMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: CALLBACK_DATA_GET_ALLEGED_TARGET_SEPARATOR in c.data,
    state=[ScheduleMenuStatesGroup.student_schedule, ScheduleMenuStatesGroup.lecturer_schedule]
)
@rate_limit(limit=RATE_LIMIT_DICT[SCHEDULE_INLINE_KEYBOARD_KEY], key=SCHEDULE_INLINE_KEYBOARD_KEY)
async def choice_alleged_target_name(callback: types.CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    try:
        async with state.proxy() as data:
            # Assign the target name chosen by the user to the variable alleged_target_name in user memory storage.
            data[ALLEGED_TARGET_NAME_KEY] = callback.data.split(CALLBACK_DATA_GET_ALLEGED_TARGET_SEPARATOR)[-1]
            # Assign target_url to the url of the weekly schedule of the selected target.
            # alleged_target_info: These are variables that store in memory storage the name of the alleged target
            # and an url to its weekly schedule.
            data[TARGET_URL_KEY] = data[ALLEGED_TARGET_INFO_KEY][data[ALLEGED_TARGET_NAME_KEY]]
            # We remove the inline keyboard for selecting the alleged target name through the zero index,
            # since this inline keyboard will always be displayed first in the work of our bot if it
            # finds more than one match for the alleged target name entered by the user.
            await bot.delete_message(
                chat_id=chat_id,
                message_id=data[SCHEDULE_INLINE_KEYBOARDS_KEY][0]
            )
            # We are clearing the history of the bot inline keyboards,
            # since there was one keyboard that we deleted step by step.
            data[SCHEDULE_INLINE_KEYBOARDS_KEY].clear()
        # Get daily schedule: check functions/get_daily_schedule.
        await get_daily_schedule(
            chat_id=chat_id,
            user_name=callback.from_user.first_name,
            daily=True,
            today=True,
            calendar=False,
            state=state
        )
    except KeyError:
        await bot.send_message(chat_id=callback.from_user.id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)
