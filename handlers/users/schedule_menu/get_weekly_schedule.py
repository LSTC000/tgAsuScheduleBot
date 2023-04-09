from data.config import RATE_LIMIT_DICT
from data.config import SCHEDULE_INLINE_KEYBOARD_KEY
from data.config import CALLBACK_DATA_GET_WEEKLY_SCHEDULE

from data.messages import START_FIND_WEEKLY_SCHEDULE_MESSAGE
from data.messages import CALLBACK_DATA_KEY_ERROR_MESSAGE

from keyboards import get_calendar_ikb

from parsers import weekly_schedule

from utils import rate_limit
from utils import create_report_weekly_schedule
from utils import processing_parser_errors
from utils import processing_parser_none_schedule_error

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
    start_find_message = await bot.send_message(chat_id=callback.from_user.id, text=START_FIND_WEEKLY_SCHEDULE_MESSAGE)

    try:
        async with state.proxy() as data:
            in_cache = False
            # Checking for a request in the schedule_cache
            key_cache = f"{data['alleged_target_name']} week"
            if key_cache in schedule_cache:
                in_cache = True
            # If the request is not in the schedule_cache then we will execute it
            if not in_cache:
                schedule = await weekly_schedule(
                    chat_id=callback.from_user.id,
                    target=data['target'],
                    target_weekly_schedule_url=data['target_url']
                )
                # Put the weekly_schedule data in the schedule_cache
                schedule_cache[key_cache] = schedule
            else:
                schedule = schedule_cache[key_cache]
            # Processing of returned data from weekly_schedule function
            # For a more detailed understanding check weekly_schedule function in parsers/weekly_schedule_parser
            if isinstance(schedule, int):
                # Processing parser errors from errors/parsers/weekly_schedule_parser except none schedule error
                msg = processing_parser_errors(
                    error_code=schedule,
                    user_name=callback.from_user.first_name,
                    target=data['target']
                )
                await bot.send_message(chat_id=callback.from_user.id, text=msg)
            elif isinstance(schedule, str):
                # Processing parser none schedule error from errors/parsers/weekly_schedule_parser
                msg = processing_parser_none_schedule_error(
                    target_weekly_schedule_url=data['target_url'],
                    user_name=callback.from_user.first_name,
                    target=data['target'],
                    daily=False,
                    today=True,
                    calendar=False
                )

                ikb = get_calendar_ikb()

                message = await bot.send_message(chat_id=callback.from_user.id, text=msg, reply_markup=ikb)
                # Add selected inline keyboard
                data['message_id_last_schedule_inline_keyboards'].append(message.message_id)
            else:
                # Create report for a weekly schedule
                report_list = create_report_weekly_schedule(
                    target=data['target'],
                    target_schedule=schedule[0],
                    target_name=data['alleged_target_name'],
                    target_url=data['target_url'],
                    target_table_headers=schedule[2]
                )

                ikb = get_calendar_ikb()

                count_reports = len(report_list) - 1
                for i, report in enumerate(report_list):
                    if i != count_reports:
                        await bot.send_message(chat_id=callback.from_user.id, text=report)
                    else:
                        message = await bot.send_message(chat_id=callback.from_user.id, text=report, reply_markup=ikb)
                        # Add selected inline keyboard
                        data['message_id_last_schedule_inline_keyboards'].append(message.message_id)
    except KeyError:
        await bot.send_message(chat_id=callback.from_user.id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=start_find_message.message_id)
