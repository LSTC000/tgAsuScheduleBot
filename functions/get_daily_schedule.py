from data.config import STUDENT_TARGET

from data.messages import START_FIND_DAILY_SCHEDULE_MESSAGE
from data.messages import CHOICE_ALLEGED_STUDENT_TARGET_MESSAGE
from data.messages import CHOICE_ALLEGED_LECTURER_TARGET_MESSAGE
from data.messages import CALLBACK_DATA_KEY_ERROR_MESSAGE

from parsers import daily_schedule

from utils import processing_parser_errors
from utils import processing_parser_none_schedule_error
from utils import create_report_daily_schedule

from keyboards import get_today_schedule_ikb
from keyboards import get_tomorrow_schedule_ikb
from keyboards import get_alleged_target_name_ikb
from keyboards import get_calendar_ikb

from loader import bot, schedule_cache

from aiogram.dispatcher import FSMContext


async def get_daily_schedule(
        chat_id: str,
        user_name: str,
        daily: bool,
        today: bool,
        calendar: bool,
        state: FSMContext
) -> None:
    '''
    :param chat_id: Telegram user chat_id
    :param user_name: Telegram user first name
    :param daily: True if you want to know the schedule for the day else False.
        If you find out the schedule using the calendar (calendar param is True) then any value
    :param today: True if you want to know the schedule for today else False.
        If you find out the weekly schedule (daily param is False) then any value.
        P.S. this function is not used in finding the weekly schedule.
        If you find out the schedule using the calendar (calendar param is True) then any value
    :param calendar: True if you want to find out the schedule using the calendar else False
    :param state: FSMContext state to use User memory storage
    :return: None
    '''

    start_find_message = await bot.send_message(chat_id=chat_id, text=START_FIND_DAILY_SCHEDULE_MESSAGE)

    try:
        async with state.proxy() as data:
            in_cache = False
            # Checking for a request in the schedule_cache
            key_cache = f"{data['alleged_target_name']} {data['target_date_query_url_code']}"
            if key_cache in schedule_cache:
                in_cache = True
            # If the request is not in the schedule_cache then we will execute it
            if not in_cache:
                schedule = await daily_schedule(
                    chat_id=chat_id,
                    target=data['target'],
                    target_url=data['target_url'],
                    alleged_target_name=data['alleged_target_name'],
                    target_date_query_url_code=data['target_date_query_url_code']
                )
                # Put the daily_schedule data in the schedule_cache
                schedule_cache[key_cache] = schedule
            else:
                schedule = schedule_cache[key_cache]
            # Processing of returned data from daily_schedule function
            # For a more detailed understanding check daily_schedule function in parsers/daily_schedule_parser
            if isinstance(schedule, int):
                # Processing parser errors from errors/parsers/daily_schedule_parser except none schedule error
                msg = processing_parser_errors(
                    error_code=schedule,
                    user_name=user_name,
                    target=data['target']
                )
                await bot.send_message(chat_id=chat_id, text=msg)
            elif isinstance(schedule, dict):
                # Processing choice alleged target name

                # These are variables that store in memory storage the name of the alleged target
                # and an url to its weekly schedule
                data['alleged_target_info'] = schedule

                if data['target'] == STUDENT_TARGET:
                    msg = CHOICE_ALLEGED_STUDENT_TARGET_MESSAGE
                else:
                    msg = CHOICE_ALLEGED_LECTURER_TARGET_MESSAGE

                alleged_target_ikb = get_alleged_target_name_ikb(data['alleged_target_info'])

                message = await bot.send_message(chat_id=chat_id, text=msg, reply_markup=alleged_target_ikb)
                # Add selected inline keyboard
                data['message_id_last_schedule_inline_keyboards'].append(message.message_id)
            elif isinstance(schedule, list):
                # Processing parser none schedule error from errors/parsers/daily_schedule_parser

                # Check this data variables in handlers/users/schedule_menu/get_today_schedule
                data['alleged_target_name'] = schedule[0]
                data['target_url'] = schedule[1]

                msg = processing_parser_none_schedule_error(
                    target_weekly_schedule_url=data['target_url'],
                    user_name=user_name,
                    target=data['target'],
                    daily=daily,
                    today=today,
                    calendar=calendar
                )
                # Check this data variables in handlers/users/schedule_menu/get_today_schedule
                if data['target_date_query_url_code'] == data['today_target_date_query_url_code']:
                    ikb = get_today_schedule_ikb()
                elif data['target_date_query_url_code'] == data['tomorrow_target_date_query_url_code']:
                    ikb = get_tomorrow_schedule_ikb()
                else:
                    ikb = get_calendar_ikb()

                message = await bot.send_message(chat_id=chat_id, text=msg, reply_markup=ikb)
                # Add selected inline keyboard
                data['message_id_last_schedule_inline_keyboards'].append(message.message_id)
            else:
                # Create report for a daily schedule

                # Check this data variables in handlers/users/schedule_menu/get_today_schedule
                data['alleged_target_name'] = schedule[1]
                data['target_url'] = schedule[2]

                report = create_report_daily_schedule(
                    target=data['target'],
                    target_schedule=schedule[0],
                    target_name=data['alleged_target_name'],
                    target_url=data['target_url'],
                    target_table_headers=schedule[3]
                )
                # Check this data variables in handlers/users/schedule_menu/get_today_schedule
                if data['target_date_query_url_code'] == data['today_target_date_query_url_code']:
                    ikb = get_today_schedule_ikb()
                elif data['target_date_query_url_code'] == data['tomorrow_target_date_query_url_code']:
                    ikb = get_tomorrow_schedule_ikb()
                else:
                    ikb = get_calendar_ikb()

                message = await bot.send_message(chat_id=chat_id, text=report, reply_markup=ikb)
                # Add selected inline keyboard
                data['message_id_last_schedule_inline_keyboards'].append(message.message_id)
    except KeyError:
        await bot.send_message(chat_id=chat_id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)

    await bot.delete_message(chat_id=chat_id, message_id=start_find_message.message_id)
