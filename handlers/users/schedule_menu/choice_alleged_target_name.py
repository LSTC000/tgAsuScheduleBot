from data.config import RATE_LIMIT_DICT
from data.config import SCHEDULE_INLINE_KEYBOARD_KEY
from data.config import CALLBACK_DATA_GET_ALLEGED_TARGET_SEPARATOR

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
    try:
        async with state.proxy() as data:
            # Assign the target name chosen by the user to the variable alleged_target_name in user memory storage
            data['alleged_target_name'] = callback.data.split(CALLBACK_DATA_GET_ALLEGED_TARGET_SEPARATOR)[-1]
            # Assign target_url to the url of the weekly schedule of the selected target
            # alleged_target_info: These are variables that store in memory storage the name of the alleged target
            # and an url to its weekly schedule
            data['target_url'] = data['alleged_target_info'][data['alleged_target_name']]
            # We remove the inline keyboard for selecting the alleged target name through the zero index,
            # since this inline keyboard will always be displayed first in the work of our bot if it
            # finds more than one match for the alleged target name entered by the user
            await bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=data['message_id_last_schedule_inline_keyboards'][0]
            )
            # We are clearing the history of the bot inline keyboards,
            # since there was one keyboard that we deleted step by step
            data['message_id_last_schedule_inline_keyboards'].clear()
        # Get daily schedule: check functions/get_daily_schedule
        await get_daily_schedule(
            chat_id=callback.from_user.id,
            user_name=callback.from_user.first_name,
            daily=True,
            today=True,
            calendar=False,
            state=state
        )
    except KeyError:
        await bot.send_message(chat_id=callback.from_user.id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)
