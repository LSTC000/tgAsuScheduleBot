from data.callbacks import CALLBACK_DATA_GET_TOMORROW_SCHEDULE

from data.redis import TARGET_DATE_QUERY_URL_CODE_KEY, TOMORROW_TARGET_DATE_QUERY_URL_CODE_KEY

from data.config import SCHEDULE_INLINE_KEYBOARD_KEY, RATE_LIMIT_DICT

from data.messages import CALLBACK_DATA_KEY_ERROR_MESSAGE

from functions import get_daily_schedule

from utils import rate_limit

from loader import dp, bot

from states import ScheduleMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CALLBACK_DATA_GET_TOMORROW_SCHEDULE,
    state=[ScheduleMenuStatesGroup.student_schedule, ScheduleMenuStatesGroup.lecturer_schedule]
)
@rate_limit(limit=RATE_LIMIT_DICT[SCHEDULE_INLINE_KEYBOARD_KEY], key=SCHEDULE_INLINE_KEYBOARD_KEY)
async def get_tomorrow_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    try:
        # Check this data variables in handlers/users/schedule_menu/get_today_schedule.
        async with state.proxy() as data:
            data[TARGET_DATE_QUERY_URL_CODE_KEY] = data[TOMORROW_TARGET_DATE_QUERY_URL_CODE_KEY]
        # Get daily schedule: check functions/get_daily_schedule.
        await get_daily_schedule(
            user_id=callback.from_user.id,
            user_name=callback.from_user.first_name,
            daily=True,
            today=False,
            calendar=False,
            state=state
        )
    except KeyError:
        await bot.send_message(chat_id=callback.from_user.id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)
