from data.config import STUDENT_TARGET

from data.redis import (
    TARGET_KEY,
    TARGET_URL_KEY,
    ALLEGED_TARGET_NAME_KEY,
    ALLEGED_TARGET_INFO_KEY,
    TARGET_DATE_QUERY_URL_CODE_KEY,
    TODAY_TARGET_DATE_QUERY_URL_CODE_KEY,
    TOMORROW_TARGET_DATE_QUERY_URL_CODE_KEY,
    SCHEDULE_INLINE_KEYBOARDS_KEY
)

from data.messages import (
    START_FIND_DAILY_SCHEDULE_MESSAGE,
    CHOICE_ALLEGED_STUDENT_TARGET_MESSAGE,
    CHOICE_ALLEGED_LECTURER_TARGET_MESSAGE,
    CALLBACK_DATA_KEY_ERROR_MESSAGE
)

from parsers import daily_schedule

from utils import processing_parser_errors, processing_parser_none_schedule_error, create_report_daily_schedule

from keyboards import (
    get_today_schedule_ikb,
    get_tomorrow_schedule_ikb,
    get_alleged_target_name_ikb,
    get_calendar_ikb
)

from loader import bot, schedule_cache

from aiogram.dispatcher import FSMContext


async def get_daily_schedule(
        user_id: int,
        user_name: str,
        daily: bool,
        today: bool,
        calendar: bool,
        state: FSMContext
) -> None:
    '''
    :param user_id: Telegram user id.
    :param user_name: Telegram user first name.
    :param daily: True if you want to know the schedule for the day else False.
        If you find out the schedule using the calendar (calendar param is True) then any value.
    :param today: True if you want to know the schedule for today else False.
        If you find out the weekly schedule (daily param is False) then any value.
        P.S. this function is not used in finding the weekly schedule.
        If you find out the schedule using the calendar (calendar param is True) then any value.
    :param calendar: True if you want to find out the schedule using the calendar else False.
    :param state: FSMContext state to use User memory storage.
    :return: None.
    '''

    start_find_message = await bot.send_message(chat_id=user_id, text=START_FIND_DAILY_SCHEDULE_MESSAGE)

    try:
        async with state.proxy() as data:
            in_cache = False
            # Checking for a request in the schedule_cache.
            key_cache = f"{data[ALLEGED_TARGET_NAME_KEY]} {data[TARGET_DATE_QUERY_URL_CODE_KEY]}"
            if key_cache in schedule_cache:
                in_cache = True
            # If the request is not in the schedule_cache then we will execute it.
            if not in_cache:
                schedule = await daily_schedule(
                    user_id=user_id,
                    target=data[TARGET_KEY],
                    target_url=data[TARGET_URL_KEY],
                    alleged_target_name=data[ALLEGED_TARGET_NAME_KEY],
                    target_date_query_url_code=data[TARGET_DATE_QUERY_URL_CODE_KEY]
                )
                # Put the daily_schedule data in the schedule_cache.
                schedule_cache[key_cache] = schedule
            else:
                schedule = schedule_cache[key_cache]
            # Processing of returned data from daily_schedule function.
            # For a more detailed understanding check daily_schedule function in parsers/daily_schedule_parser.
            if isinstance(schedule, int):
                # Processing parser errors from errors/parsers/daily_schedule_parser except none schedule error.
                msg = processing_parser_errors(
                    error_code=schedule,
                    user_name=user_name,
                    target=data[TARGET_KEY]
                )
                await bot.send_message(chat_id=user_id, text=msg)
            elif isinstance(schedule, dict):
                # Processing choice alleged target name.

                # These are variables that store in memory storage the name of the alleged target
                # and an url to its weekly schedule.
                data[ALLEGED_TARGET_INFO_KEY] = schedule

                if data[TARGET_KEY] == STUDENT_TARGET:
                    msg = CHOICE_ALLEGED_STUDENT_TARGET_MESSAGE
                else:
                    msg = CHOICE_ALLEGED_LECTURER_TARGET_MESSAGE

                alleged_target_ikb = get_alleged_target_name_ikb(data[ALLEGED_TARGET_INFO_KEY])

                message = await bot.send_message(chat_id=user_id, text=msg, reply_markup=alleged_target_ikb)
                # Add selected inline keyboard.
                data[SCHEDULE_INLINE_KEYBOARDS_KEY].append(message.message_id)
            elif isinstance(schedule, list):
                # Processing parser none schedule error from errors/parsers/daily_schedule_parser.

                # Check this data variables in handlers/users/schedule_menu/get_today_schedule.
                data[ALLEGED_TARGET_NAME_KEY] = schedule[0]
                data[TARGET_URL_KEY] = schedule[1]

                msg = processing_parser_none_schedule_error(
                    target_weekly_schedule_url=data[TARGET_URL_KEY],
                    user_name=user_name,
                    target=data[TARGET_KEY],
                    daily=daily,
                    today=today,
                    calendar=calendar
                )
                # Check this data variables in handlers/users/schedule_menu/get_today_schedule.
                if data[TARGET_DATE_QUERY_URL_CODE_KEY] == data[TODAY_TARGET_DATE_QUERY_URL_CODE_KEY]:
                    ikb = get_today_schedule_ikb()
                elif data[TARGET_DATE_QUERY_URL_CODE_KEY] == data[TOMORROW_TARGET_DATE_QUERY_URL_CODE_KEY]:
                    ikb = get_tomorrow_schedule_ikb()
                else:
                    ikb = get_calendar_ikb()

                message = await bot.send_message(chat_id=user_id, text=msg, reply_markup=ikb)
                # Add selected inline keyboard.
                data[SCHEDULE_INLINE_KEYBOARDS_KEY].append(message.message_id)
            else:
                # Create report for a daily schedule.

                # Check this data variables in handlers/users/schedule_menu/get_today_schedule.
                data[ALLEGED_TARGET_NAME_KEY] = schedule[1]
                data[TARGET_URL_KEY] = schedule[2]

                report = create_report_daily_schedule(
                    target=data[TARGET_KEY],
                    target_schedule=schedule[0],
                    target_name=data[ALLEGED_TARGET_NAME_KEY],
                    target_url=data[TARGET_URL_KEY],
                    target_table_headers=schedule[3]
                )
                # Check this data variables in handlers/users/schedule_menu/get_today_schedule.
                if data[TARGET_DATE_QUERY_URL_CODE_KEY] == data[TODAY_TARGET_DATE_QUERY_URL_CODE_KEY]:
                    ikb = get_today_schedule_ikb()
                elif data[TARGET_DATE_QUERY_URL_CODE_KEY] == data[TOMORROW_TARGET_DATE_QUERY_URL_CODE_KEY]:
                    ikb = get_tomorrow_schedule_ikb()
                else:
                    ikb = get_calendar_ikb()

                message = await bot.send_message(chat_id=user_id, text=report, reply_markup=ikb)
                # Add selected inline keyboard.
                data[SCHEDULE_INLINE_KEYBOARDS_KEY].append(message.message_id)
    except KeyError:
        await bot.send_message(chat_id=user_id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)

    await bot.delete_message(chat_id=user_id, message_id=start_find_message.message_id)
