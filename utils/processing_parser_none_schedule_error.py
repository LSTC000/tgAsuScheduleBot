from data.urls import SCHEDULE_ASU_URL
from data.config import STUDENT_TARGET, LECTURER_TARGET

from data.messages import GET_DAILY_SCHEDULE_DICT_TODAY_NONE_SCHEDULE_ERROR_STUDENT_MESSAGE
from data.messages import GET_DAILY_SCHEDULE_DICT_TOMORROW_NONE_SCHEDULE_ERROR_STUDENT_MESSAGE
from data.messages import GET_DAILY_SCHEDULE_DICT_CALENDAR_NONE_SCHEDULE_ERROR_STUDENT_MESSAGE
from data.messages import GET_WEEKLY_SCHEDULE_LIST_NONE_SCHEDULE_ERROR_STUDENT_MESSAGE

from data.messages import GET_DAILY_SCHEDULE_DICT_TODAY_NONE_SCHEDULE_ERROR_LECTURER_MESSAGE
from data.messages import GET_DAILY_SCHEDULE_DICT_TOMORROW_NONE_SCHEDULE_ERROR_LECTURER_MESSAGE
from data.messages import GET_DAILY_SCHEDULE_DICT_CALENDAR_NONE_SCHEDULE_ERROR_LECTURER_MESSAGE
from data.messages import GET_WEEKLY_SCHEDULE_LIST_NONE_SCHEDULE_ERROR_LECTURER_MESSAGE


def processing_parser_none_schedule_error(
        target_weekly_schedule_url: str,
        user_name: str,
        target: str,
        daily: bool,
        today: bool,
        calendar: bool
) -> str:
    '''
    :param target_weekly_schedule_url: Url to the weekly target schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/
    :param user_name: Telegram user first name
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config
    :param daily: True if you output a message about none daily schedule else False.
        If you output a message about none calendar schedule (calendar param is True) then any value
    :param today: True if you output a message about none today daily schedule else False.
        If you output a message about none weekly schedule (daily param is False) then any value.
        If you output a message about none calendar schedule (calendar param is True) then any value
    :param calendar: True if you output a message about none calendar schedule else False
    :return: Message about none schedule
    '''

    if target == STUDENT_TARGET:
        if calendar:
            return GET_DAILY_SCHEDULE_DICT_CALENDAR_NONE_SCHEDULE_ERROR_STUDENT_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        else:
            if daily:
                if today:
                    return GET_DAILY_SCHEDULE_DICT_TODAY_NONE_SCHEDULE_ERROR_STUDENT_MESSAGE.format(
                        user_name,
                        target_weekly_schedule_url
                    )
                else:
                    return GET_DAILY_SCHEDULE_DICT_TOMORROW_NONE_SCHEDULE_ERROR_STUDENT_MESSAGE.format(
                        user_name,
                        target_weekly_schedule_url
                    )
            else:
                return GET_WEEKLY_SCHEDULE_LIST_NONE_SCHEDULE_ERROR_STUDENT_MESSAGE.format(
                    user_name,
                    target_weekly_schedule_url
                )
    else:
        if calendar:
            return GET_DAILY_SCHEDULE_DICT_CALENDAR_NONE_SCHEDULE_ERROR_LECTURER_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        else:
            if daily:
                if today:
                    return GET_DAILY_SCHEDULE_DICT_TODAY_NONE_SCHEDULE_ERROR_LECTURER_MESSAGE.format(
                        user_name,
                        target_weekly_schedule_url
                    )
                else:
                    return GET_DAILY_SCHEDULE_DICT_TOMORROW_NONE_SCHEDULE_ERROR_LECTURER_MESSAGE.format(
                        user_name,
                        target_weekly_schedule_url
                    )
            else:
                return GET_WEEKLY_SCHEDULE_LIST_NONE_SCHEDULE_ERROR_LECTURER_MESSAGE.format(
                    user_name,
                    target_weekly_schedule_url
                )
