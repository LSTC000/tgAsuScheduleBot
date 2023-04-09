from data.config import RATE_LIMIT_DICT
from data.config import SCHEDULE_INLINE_KEYBOARD_KEY
from data.config import CALLBACK_DATA_GET_TOMORROW_SCHEDULE

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
        # Check this data variables in handlers/users/schedule_menu/get_today_schedule
        async with state.proxy() as data:
            data['target_date_query_url_code'] = data['tomorrow_target_date_query_url_code']
        # Get daily schedule: check functions/get_daily_schedule
        await get_daily_schedule(
            chat_id=callback.from_user.id,
            user_name=callback.from_user.first_name,
            daily=True,
            today=False,
            calendar=False,
            state=state
        )
    except KeyError:
        await bot.send_message(chat_id=callback.from_user.id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)
