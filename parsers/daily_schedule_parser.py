import json
from typing import Union, List, Tuple
from datetime import datetime
from urllib.parse import quote

from data.config import (
    REQUEST_HEADERS,
    STUDENT_TARGET,
    STUDENT_TABLE_HEADERS,
    LECTURER_TABLE_HEADERS,
    COUNT_SHOW_ALLEGED_TARGETS_THRESHOLD,
    JSON_TOKEN
)

from errors import (
    GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_CODE,
    GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_CODE,
    GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_CODE,
    GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_CODE,
    GET_DAILY_SCHEDULE_DICT_NONE_SCHEDULE_ERROR_CODE
)

from data.urls import (
    JSON_DATE_QUERY_URL,
    STUDENTS_URL,
    LECTURERS_URL,
    JSON_STUDENTS_QUERY_URL,
    JSON_LECTURERS_QUERY_URL,
    FREE_ROOMS_URL_DICT
)

import httpx


async def get_alleged_targets_urls_dict(user_id: int, target: str, alleged_target_url: str) -> Union[int, dict]:
    '''
    :param user_id: Telegram user id.
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config.
    :param alleged_target_url: Url to search for the alleged targets.
        Example: https://www.asu.ru/timetable/search/students/?query=404.
    :return:
        Int - If any error get_alleged_targets_urls_dict was caused.
        Dict - Contains the key - the full name of the alleged target and the value - an url to the weekly
            target schedule.
    '''

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=alleged_target_url, headers=REQUEST_HEADERS, params={'chat_id': user_id})
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_CODE

    try:
        data = response.json()
        if target == STUDENT_TARGET:
            groups_data = data.get('groups')
            rows = groups_data.get('rows')

            # Checking for the number of matches found with the name of the alleged target.
            if not rows:
                return GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_CODE
            # Checking for an acceptable threshold for the number of possible alleged targets.
            if rows > COUNT_SHOW_ALLEGED_TARGETS_THRESHOLD:
                return GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_CODE

            records = groups_data.get('records')
            urls_dict = {}

            for record in records:
                urls_dict[record.get('groupCode')] = STUDENTS_URL.format(record.get('path'))

            return urls_dict
        else:
            lecturers_data = data.get('lecturers')
            rows = lecturers_data.get('rows')

            # Checking for the number of matches found with the name of the alleged target.
            if not rows:
                return GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_CODE
            # Checking for an acceptable threshold for the number of possible alleged targets.
            if rows > COUNT_SHOW_ALLEGED_TARGETS_THRESHOLD:
                return GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_CODE

            records = lecturers_data.get('records')
            urls_dict = {}

            for record in records:
                try:
                    key = f"{record.get('lecturerName')} ({record.get('lecturerPosition')})"
                except KeyError:
                    key = f"{record.get('lecturerName')}"

                urls_dict[key] = LECTURERS_URL.format(record.get('path'))

            return urls_dict
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError, FileNotFoundError, IOError):
        return GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_CODE


async def get_daily_schedule_dict(
        user_id: int,
        target: str,
        url: str,
        date_query_url_code: str,
        table_headers: list
) -> Union[int, dict]:
    '''
    :param user_id: Telegram user id.
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config.
    :param url: Url to the weekly target schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param date_query_url_code: Url code for finding a schedule for today.
        Example: '20230326'.
    :param table_headers: STUDENT_TABLE_HEADERS or LECTURER_TABLE_HEADERS from data/config/parsers/config.
    :return:
        Int - If any error get_daily_schedule_dict was caused.
        Dict - Contains the key - the name of the table header and the value - the header data.
    '''

    # Create an url to find the daily schedule.
    date_query_url = JSON_DATE_QUERY_URL.format(url, date_query_url_code, JSON_TOKEN)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=date_query_url, headers=REQUEST_HEADERS, params={'chat_id': user_id})
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_CODE

    try:
        data = response.json()
        schedule_data = data.get('schedule')

        rows = schedule_data.get('rows')

        # Checking whether there are classes today or not.
        if not rows:
            return GET_DAILY_SCHEDULE_DICT_NONE_SCHEDULE_ERROR_CODE

        records = schedule_data.get('records')

        if target == STUDENT_TARGET:
            schedule = {
                table_headers[0]: datetime.strptime(date_query_url_code, "%Y%m%d").strftime("%a %d-%m-%Y"),
                table_headers[1]: [],
                table_headers[2]: [],
                table_headers[3]: [],
                table_headers[4]: [],
                table_headers[5]: [],
                table_headers[6]: []
            }

            for record in records:
                # Add lesson num.
                try:
                    schedule[table_headers[1]].append(record.get('lessonNum'))
                except KeyError:
                    schedule[table_headers[1]].append('')
                # Add lesson time.
                try:
                    schedule[table_headers[2]].append(f"{record.get('lessonTimeStart')} - {record.get('lessonTimeEnd')}")
                except KeyError:
                    schedule[table_headers[2]].append('')
                # Add lesson subject.
                try:
                    subject = record.get('lessonSubject')
                    try:
                        lesson_group = record.get('lessonGroups')[0].get('lessonSubGroup')
                        subject_type = record.get('lessonSubjectType')
                        if lesson_group:
                            schedule[table_headers[3]].append(lesson_group + ' ' + subject_type + ' ' + subject.get('subjectTitle'))
                        else:
                            schedule[table_headers[3]].append(subject_type + ' ' + subject.get('subjectTitle'))
                    except (KeyError, IndexError):
                        schedule[table_headers[3]].append(subject.get('subjectTitle'))
                except KeyError:
                    schedule[table_headers[3]].append('')
                # Add lesson lecturers.
                try:
                    lecturers = record.get('lessonLecturers')
                    lecturers_list = []

                    for lecturer in lecturers:
                        lecturers_list.append(f"{lecturer.get('lecturerName')} ({lecturer.get('lecturerPosition')})")

                    schedule[table_headers[4]].append(', '.join(lecturers_list))
                except KeyError:
                    schedule[table_headers[4]].append('')
                # Add lesson room.
                try:
                    room = record.get('lessonRoom')
                    schedule[table_headers[5]].append(f"{room.get('roomTitle')} {room.get('roomBuildingCode')}")
                except KeyError:
                    schedule[table_headers[5]].append('')
                # Add url to free rooms.
                try:
                    room = record.get('lessonRoom')
                    building_code = room.get('roomBuildingCode').lower()
                    if building_code in FREE_ROOMS_URL_DICT:
                        lesson_time = record.get('lessonTimeStart').replace(':', '') + record.get('lessonTimeEnd').replace(':', '')
                        lesson_num = int(record.get('lessonNum'))
                        lesson_num = f'0{lesson_num}' if lesson_num < 10 else f'{lesson_num}'
                        schedule[table_headers[6]].append(FREE_ROOMS_URL_DICT[building_code].format(date_query_url_code + lesson_time + lesson_num))
                    else:
                        schedule[table_headers[6]].append('')
                except KeyError:
                    schedule[table_headers[6]].append('')

            return schedule
        else:
            schedule = {
                table_headers[0]: datetime.strptime(date_query_url_code, "%Y%m%d").strftime("%a %d-%m-%Y"),
                table_headers[1]: [],
                table_headers[2]: [],
                table_headers[3]: [],
                table_headers[4]: [],
                table_headers[5]: [],
                table_headers[6]: []
            }

            for record in records:
                # Add lesson num.
                try:
                    schedule[table_headers[1]].append(record.get('lessonNum'))
                except KeyError:
                    schedule[table_headers[1]].append('')
                # Add lesson time.
                try:
                    schedule[table_headers[2]].append(f"{record.get('lessonTimeStart')} - {record.get('lessonTimeEnd')}")
                except KeyError:
                    schedule[table_headers[2]].append('')
                # Add lesson subject.
                try:
                    subject = record.get('lessonSubject')
                    try:
                        subject_type = record.get('lessonSubjectType')
                        schedule[table_headers[3]].append(subject_type + ' ' + subject.get('subjectTitle'))
                    except KeyError:
                        schedule[table_headers[3]].append(subject.get('subjectTitle'))
                except KeyError:
                    schedule[table_headers[3]].append('')
                # Add lesson groups.
                try:
                    groups = record.get('lessonGroups')
                    groups_list = []

                    for group in groups:
                        groups_list.append(group.get('lessonGroup').get('groupCode') + ' ' + group.get('lessonSubGroup'))

                    schedule[table_headers[4]].append(', '.join(groups_list))
                except KeyError:
                    schedule[table_headers[4]].append('')
                # Add lesson room.
                try:
                    room = record.get('lessonRoom')
                    schedule[table_headers[5]].append(f"{room.get('roomTitle')} {room.get('roomBuildingCode')}")
                except KeyError:
                    schedule[table_headers[5]].append('')
                # Add url to free rooms.
                try:
                    room = record.get('lessonRoom')
                    building_code = room.get('roomBuildingCode').lower()
                    if building_code in FREE_ROOMS_URL_DICT:
                        lesson_time = record.get('lessonTimeStart').replace(':', '') + record.get('lessonTimeEnd').replace(':', '')
                        lesson_num = int(record.get('lessonNum'))
                        lesson_num = f'0{lesson_num}' if lesson_num < 10 else f'{lesson_num}'
                        schedule[table_headers[6]].append(FREE_ROOMS_URL_DICT[building_code].format(date_query_url_code + lesson_time + lesson_num))
                    else:
                        schedule[table_headers[6]].append('')
                except KeyError:
                    schedule[table_headers[6]].append('')

            return schedule
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError, FileNotFoundError, IOError):
        return GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_CODE


async def get_daily_schedule_data(
        user_id: int,
        target: str,
        target_url: str,
        alleged_target_name: str,
        target_date_query_url_code: str,
        target_query_url: str,
        target_table_headers: list
) -> Union[int, List[str], dict, Tuple[dict, str, str, list]]:
    '''
    :param user_id: Telegram user id.
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config.
    :param target_url: Url to the weekly target schedule. From it you can get an url to the schedule of a certain day,
        if you add to its end DATE_QUERY_URL from data/urls/urls.
        Until we called the get_daily_schedule_data function equals None.
        If any error from the get_alleged_targets_urls_dict function is called the target_url will remain equal to None.
        Example: None or https://www.asu.ru/timetable/students/21/2129440242/.
    :param alleged_target_name: This is the alleged name of the target because at the beginning we cannot say
        the exact name of the target, since the user can enter an incomplete name of the target and
        then the bot will offer him a choice on the inline keyboard.
        Example: 'Дронов' or 'Мих'.
    :param target_date_query_url_code: Url code for finding a schedule for today.
        Example: '20230326'.
    :param target_query_url: JSON_STUDENTS_QUERY_URL or JSON_LECTURERS_QUERY_URL from data/urls/urls.
    :param target_table_headers: STUDENT_TABLE_HEADERS or LECTURER_TABLE_HEADERS from data/config/parsers/config.
    :return:
        Int - if any error was caused other than none schedule. Contains an error code that will be processed in
            processing_parser_errors function from utils/processing_parser_errors.
        List - if the none schedule error was caused. Сontains the full name of the target and an url to its weekly
            schedule, so that when we search for a schedule for tomorrow, for the current week or by calendar,
            we do not have to search for this information again. This error is processed in
            processing_parser_none_schedule_error function from utils/processing_parser_none_schedule_error.
        Dict - Contains the key - the name of the alleged target and the value of the key - a link to the weekly
            target schedule.
        Tuple - Contains a dictionary with data about the daily schedule, the full name of the target, an url to the
            weekly schedule of the target and the name of the schedule columns to create report schedule.
    '''

    # If the url to the weekly target schedule is already known, then you don't have to search for it again.
    if target_url is None:
        # Create an url to search for the alleged targets.
        # The line below is in order to get the URL-encoded string for the alleged target name.
        alleged_target_name_encoded = quote(alleged_target_name, safe='+:/?=&')
        target_query_url = target_query_url.format(alleged_target_name_encoded, JSON_TOKEN)

        alleged_targets_urls_dict = await get_alleged_targets_urls_dict(
            user_id=user_id,
            target=target,
            alleged_target_url=target_query_url
        )
        # If any error was caused in the get_alleged_targets_urls_dict function.
        if isinstance(alleged_targets_urls_dict, int):
            return alleged_targets_urls_dict
        # If we received from get_alleged_targets_urls_dict more than one alleged target.
        if len(alleged_targets_urls_dict) > 1:
            return alleged_targets_urls_dict
        # Else get the key and an url to the weekly schedule.
        for key in alleged_targets_urls_dict.keys():
            target_name = key
            target_url = alleged_targets_urls_dict[key]
    else:
        target_name = alleged_target_name

    daily_schedule_dict = await get_daily_schedule_dict(
        user_id=user_id,
        target=target,
        url=target_url,
        date_query_url_code=target_date_query_url_code,
        table_headers=target_table_headers
    )
    # If any error was caused in the get_daily_schedule_dict function.
    if isinstance(daily_schedule_dict, int):
        # If none schedule error was caused in the get_daily_schedule_dict function.
        if daily_schedule_dict == GET_DAILY_SCHEDULE_DICT_NONE_SCHEDULE_ERROR_CODE:
            return [target_name, target_url]

        return daily_schedule_dict

    return daily_schedule_dict, target_name, target_url, target_table_headers


async def daily_schedule(
        user_id: int,
        target: str,
        target_url: str,
        alleged_target_name: str,
        target_date_query_url_code: str
) -> Union[int, List[str], dict, Tuple[dict, str, str, list]]:
    '''
    :param user_id: Telegram user id.
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config.
    :param target_url: Url to the weekly target schedule. From it you can get an url to the schedule of a certain day,
        if you add to its end DATE_QUERY_URL from data/urls/urls.
        Until we called the get_daily_schedule_data function equals None.
        Example: None or https://www.asu.ru/timetable/students/21/2129440242/.
    :param alleged_target_name: This is the alleged name of the target because at the beginning we cannot say
        the exact name of the target, since the user can enter an incomplete name of the target and
        then the bot will offer him a choice on the inline keyboard.
        Example: 'Дронов' or 'Мих'.
    :param target_date_query_url_code: Url code for finding a schedule for today.
        Example: '20230326'.
    :return:
        Int - if any error was caused other than none schedule. Contains an error code that will be processed in
            processing_parser_errors function from utils/processing_parser_errors.
        List - if the none schedule error was caused. Сontains the full name of the target and an url to its weekly
            schedule, so that when we search for a schedule for tomorrow, for the current week or by calendar,
            we do not have to search for this information again. This error is processed in
            processing_parser_none_schedule_error function from utils/processing_parser_none_schedule_error.
        Dict - Contains the key - the name of the alleged target and the value of the key - a link to the weekly
            target schedule.
        Tuple - Contains a dictionary with data about the daily schedule, the full name of the target, an url to the
            weekly schedule of the target and the name of the schedule columns to create report schedule.
            weekly schedule of the target and the name of the schedule columns to create report schedule.
    '''

    if target == STUDENT_TARGET:
        return await get_daily_schedule_data(
            user_id=user_id,
            target=target,
            target_url=target_url,
            alleged_target_name=alleged_target_name,
            target_date_query_url_code=target_date_query_url_code,
            target_query_url=JSON_STUDENTS_QUERY_URL,
            target_table_headers=STUDENT_TABLE_HEADERS
        )
    else:
        return await get_daily_schedule_data(
            user_id=user_id,
            target=target,
            target_url=target_url,
            alleged_target_name=alleged_target_name,
            target_date_query_url_code=target_date_query_url_code,
            target_query_url=JSON_LECTURERS_QUERY_URL,
            target_table_headers=LECTURER_TABLE_HEADERS
        )
