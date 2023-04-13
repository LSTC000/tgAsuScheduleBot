from datetime import datetime

from data.callbacks import (
    CALLBACK_DATA_GET_CALENDAR,
    CALLBACK_DATA_GET_CALENDAR_SCHEDULE,
    CALLBACK_DATA_GET_CALENDAR_SCHEDULE_SEPARATOR,
)

from data.memory_storage import (
    TARGET_DATE_QUERY_URL_CODE_KEY,
    INLINE_CALENDAR_KEY
)

from data.config import RATE_LIMIT_DICT, SCHEDULE_INLINE_KEYBOARD_KEY

from data.messages import CALENDAR_CHOICE_DATE_MESSAGE, CALENDAR_SELECTED_DATE_MESSAGE, CALLBACK_DATA_KEY_ERROR_MESSAGE

from functions import get_daily_schedule

from utils import rate_limit

from inline_calendar import InlineCalendar

from loader import dp, bot

from states import ScheduleMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CALLBACK_DATA_GET_CALENDAR,
    state=[ScheduleMenuStatesGroup.student_schedule, ScheduleMenuStatesGroup.lecturer_schedule]
)
@rate_limit(limit=RATE_LIMIT_DICT[SCHEDULE_INLINE_KEYBOARD_KEY], key=SCHEDULE_INLINE_KEYBOARD_KEY)
async def get_calendar(callback: types.CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    # Delete the last calendar inline keyboard if there is one.
    async with state.proxy() as data:
        if data[INLINE_CALENDAR_KEY] is not None:
            await bot.delete_message(chat_id=chat_id, message_id=data[INLINE_CALENDAR_KEY])
    # Calling the calendar inline keyboard.
    # Check inline_calendar/inline_calendar.
    message = await bot.send_message(
        chat_id=chat_id,
        text=CALENDAR_CHOICE_DATE_MESSAGE,
        reply_markup=await InlineCalendar().start_calendar(
            year=datetime.now().year,
            month=datetime.now().month,
            state=state
        )
    )
    # Remember calendar inline keyboard.
    async with state.proxy() as data:
        data[INLINE_CALENDAR_KEY] = message.message_id


@dp.callback_query_handler(
    lambda c: c.data in CALLBACK_DATA_GET_CALENDAR_SCHEDULE or CALLBACK_DATA_GET_CALENDAR_SCHEDULE_SEPARATOR in c.data,
    state=[ScheduleMenuStatesGroup.student_schedule, ScheduleMenuStatesGroup.lecturer_schedule]
)
@rate_limit(limit=RATE_LIMIT_DICT[SCHEDULE_INLINE_KEYBOARD_KEY], key=SCHEDULE_INLINE_KEYBOARD_KEY)
async def get_calendar_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    # Check inline_calendar/inline_calendar.
    selected, calendar_date = await InlineCalendar().process_selection(
        callback=callback,
        callback_data=callback.data,
        state=state
    )

    if selected:
        await bot.send_message(
            chat_id=chat_id,
            text=CALENDAR_SELECTED_DATE_MESSAGE.format(calendar_date.strftime('%d-%m-%Y'))
        )

        try:
            async with state.proxy() as data:
                # Check this data variable in handlers/users/schedule_menu/get_today_schedule.
                data[TARGET_DATE_QUERY_URL_CODE_KEY] = calendar_date.strftime('%Y%m%d')
            # Get daily schedule: check functions/get_daily_schedule.
            await get_daily_schedule(
                chat_id=chat_id,
                user_name=callback.from_user.first_name,
                daily=True,
                today=False,
                calendar=True,
                state=state
            )
        except KeyError:
            await bot.send_message(chat_id=chat_id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)
