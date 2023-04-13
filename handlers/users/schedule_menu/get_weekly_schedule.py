from data.callbacks import CALLBACK_DATA_GET_WEEKLY_SCHEDULE

from data.config import SCHEDULE_INLINE_KEYBOARD_KEY, RATE_LIMIT_DICT

from data.messages import CALLBACK_DATA_KEY_ERROR_MESSAGE, START_FIND_WEEKLY_SCHEDULE_MESSAGE

from keyboards import get_calendar_ikb

from parsers import weekly_schedule

from utils import (
    rate_limit,
    create_report_weekly_schedule,
    processing_parser_errors,
    processing_parser_none_schedule_error
)

from loader import dp, bot, schedule_cache

from states import ScheduleMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CALLBACK_DATA_GET_WEEKLY_SCHEDULE,
    state=[ScheduleMenuStatesGroup.student_schedule, ScheduleMenuStatesGroup.lecturer_schedule]
)
@rate_limit(limit=RATE_LIMIT_DICT[SCHEDULE_INLINE_KEYBOARD_KEY], key=SCHEDULE_INLINE_KEYBOARD_KEY)
async def get_weekly_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    start_find_message = await bot.send_message(chat_id=user_id, text=START_FIND_WEEKLY_SCHEDULE_MESSAGE)

    try:
        async with state.proxy() as data:
            in_cache = False
            # Checking for a request in the schedule_cache.
            key_cache = f"{data['alleged_target_name']} week"
            if key_cache in schedule_cache:
                in_cache = True
            # If the request is not in the schedule_cache then we will execute it.
            if not in_cache:
                schedule = await weekly_schedule(
                    chat_id=user_id,
                    target=data['target'],
                    target_weekly_schedule_url=data['target_url']
                )
                # Put the weekly_schedule data in the schedule_cache.
                schedule_cache[key_cache] = schedule
            else:
                schedule = schedule_cache[key_cache]
            # Processing of returned data from weekly_schedule function.
            # For a more detailed understanding check weekly_schedule function in parsers/weekly_schedule_parser.
            if isinstance(schedule, int):
                # Processing parser errors from errors/parsers/weekly_schedule_parser except none schedule error.
                msg = processing_parser_errors(
                    error_code=schedule,
                    user_name=callback.from_user.first_name,
                    target=data['target']
                )
                await bot.send_message(chat_id=user_id, text=msg)
            elif isinstance(schedule, str):
                # Processing parser none schedule error from errors/parsers/weekly_schedule_parser.
                msg = processing_parser_none_schedule_error(
                    target_weekly_schedule_url=data['target_url'],
                    user_name=callback.from_user.first_name,
                    target=data['target'],
                    daily=False,
                    today=True,
                    calendar=False
                )

                message = await bot.send_message(chat_id=user_id, text=msg, reply_markup=get_calendar_ikb())
                # Add selected inline keyboard.
                data['message_id_last_schedule_inline_keyboards'].append(message.message_id)
            else:
                # Create report for a weekly schedule.
                report_list = create_report_weekly_schedule(
                    target=data['target'],
                    target_schedule=schedule[0],
                    target_name=data['alleged_target_name'],
                    target_table_headers=schedule[2]
                )

                count_reports = len(report_list) - 1
                for i, report in enumerate(report_list):
                    if i != count_reports:
                        await bot.send_message(chat_id=user_id, text=report)
                    else:
                        message = await bot.send_message(chat_id=user_id, text=report, reply_markup=get_calendar_ikb())
                        # Add selected inline keyboard.
                        data['message_id_last_schedule_inline_keyboards'].append(message.message_id)
    except KeyError:
        await bot.send_message(chat_id=user_id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)

    await bot.delete_message(chat_id=user_id, message_id=start_find_message.message_id)
