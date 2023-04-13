import json
from typing import Union, List, Tuple
from datetime import datetime

from data.config import (
    REQUEST_HEADERS,
    STUDENT_TARGET,
    STUDENT_TABLE_HEADERS,
    LECTURER_TABLE_HEADERS,
    JSON_TOKEN
)

from errors import GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_CODE, GET_WEEKLY_SCHEDULE_LIST_NONE_SCHEDULE_ERROR_CODE

from data.urls import JSON_WEEKLY_SCHEDULE_URL, FREE_ROOMS_URL_DICT

import httpx


async def get_weekly_schedule_list(
        chat_id: str,
        target: str,
        url: str,
        table_headers: list
) -> Union[int, List[dict]]:
    '''
    :param chat_id: Telegram user chat_id.
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config.
    :param url: Url to the weekly target schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param table_headers: STUDENT_TABLE_HEADERS or LECTURER_TABLE_HEADERS from data/config/parsers/config.
    :return:
        Int - If any error get_weekly_schedule_list was caused.
        List - Contains a dictionary for each day in the weekly schedule, in which the key - the name of the table
            header and the value - the header data.
    '''

    url = JSON_WEEKLY_SCHEDULE_URL.format(url, JSON_TOKEN)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, headers=REQUEST_HEADERS, params={'chat_id': chat_id})
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_CODE

    try:
        data = response.json()
        schedule_data = data.get('schedule')

        rows = schedule_data.get('rows')

        # Checking whether there are classes for this week or not.
        if not rows:
            return GET_WEEKLY_SCHEDULE_LIST_NONE_SCHEDULE_ERROR_CODE

        records = schedule_data.get('records')
        schedule_list = []

        if target == STUDENT_TARGET:
            now_date = records[0].get('lessonDate')

            schedule = {
                table_headers[0]: datetime.strptime(now_date, "%Y%m%d").strftime("%a %d-%m-%Y"),
                table_headers[1]: [],
                table_headers[2]: [],
                table_headers[3]: [],
                table_headers[4]: [],
                table_headers[5]: [],
                table_headers[6]: []
            }

            for record in records:
                prev_date = now_date
                now_date = record.get('lessonDate')

                if now_date != prev_date:
                    schedule_list.append(schedule)

                    schedule = {
                        table_headers[0]: datetime.strptime(now_date, "%Y%m%d").strftime("%a %d-%m-%Y"),
                        table_headers[1]: [],
                        table_headers[2]: [],
                        table_headers[3]: [],
                        table_headers[4]: [],
                        table_headers[5]: [],
                        table_headers[6]: []
                    }
                # Add lesson num.
                try:
                    schedule[table_headers[1]].append(record.get('lessonNum'))
                except KeyError:
                    schedule[table_headers[1]].append('')
                # Add lesson time.
                try:
                    schedule[table_headers[2]].append(
                        f"{record.get('lessonTimeStart')} - {record.get('lessonTimeEnd')}")
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
                        schedule[table_headers[6]].append(FREE_ROOMS_URL_DICT[building_code].format(now_date + lesson_time + lesson_num))
                    else:
                        schedule[table_headers[6]].append('')
                except KeyError:
                    schedule[table_headers[6]].append('')
            # For the last day of the week.
            schedule_list.append(schedule)

            return schedule_list
        else:
            now_date = records[0].get('lessonDate')

            schedule = {
                table_headers[0]: datetime.strptime(now_date, "%Y%m%d").strftime("%a %d-%m-%Y"),
                table_headers[1]: [],
                table_headers[2]: [],
                table_headers[3]: [],
                table_headers[4]: [],
                table_headers[5]: [],
                table_headers[6]: []
            }

            for record in records:
                prev_date = now_date
                now_date = record.get('lessonDate')

                if now_date != prev_date:
                    schedule_list.append(schedule)

                    schedule = {
                        table_headers[0]: datetime.strptime(now_date, "%Y%m%d").strftime("%a %d-%m-%Y"),
                        table_headers[1]: [],
                        table_headers[2]: [],
                        table_headers[3]: [],
                        table_headers[4]: [],
                        table_headers[5]: [],
                        table_headers[6]: []
                    }
                # Add lesson num.
                try:
                    schedule[table_headers[1]].append(record.get('lessonNum'))
                except KeyError:
                    schedule[table_headers[1]].append('')
                # Add lesson time.
                try:
                    schedule[table_headers[2]].append(
                        f"{record.get('lessonTimeStart')} - {record.get('lessonTimeEnd')}")
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
                        schedule[table_headers[6]].append(FREE_ROOMS_URL_DICT[building_code].format(now_date + lesson_time + lesson_num))
                    else:
                        schedule[table_headers[6]].append('')
                except KeyError:
                    schedule[table_headers[6]].append('')
            # For the last day of the week.
            schedule_list.append(schedule)

            return schedule_list
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError, FileNotFoundError, IOError):
        return GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_CODE


async def get_weekly_schedule_data(
        chat_id: str,
        target: str,
        target_weekly_schedule_url: str,
        target_table_headers: list
) -> Union[int, str, Tuple[List[dict], str, list]]:
    '''
    :param chat_id: Telegram user chat_id.
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config.
    :param target_weekly_schedule_url: Url to the weekly target schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :param target_table_headers: STUDENT_TABLE_HEADERS or LECTURER_TABLE_HEADERS from data/config/parsers/config.
    :return:
        Int - if any error was caused other than none schedule. Contains an error code that will be processed in
            processing_parser_errors function from utils/processing_parser_errors.
        Str - if the none schedule error was caused. Сontains the url to weekly schedule. This error is processed in
            processing_parser_none_schedule_error function from utils/processing_parser_none_schedule_error.
        Tuple - Contains a list with data for each day in the weekly schedule, a link to the weekly schedule and
            the names of columns to create schedule report.
    '''

    weekly_schedule_list = await get_weekly_schedule_list(
        chat_id=chat_id,
        target=target,
        url=target_weekly_schedule_url,
        table_headers=target_table_headers
    )
    # If any error was caused in the get_weekly_schedule_list function.
    if isinstance(weekly_schedule_list, int):
        # If none schedule error was caused in the get_weekly_schedule_list function.
        if weekly_schedule_list == GET_WEEKLY_SCHEDULE_LIST_NONE_SCHEDULE_ERROR_CODE:
            return target_weekly_schedule_url

        return weekly_schedule_list

    return weekly_schedule_list, target_weekly_schedule_url, target_table_headers


async def weekly_schedule(
        chat_id: str,
        target: str,
        target_weekly_schedule_url: str
) -> Union[int, str, Tuple[List[dict], str, list]]:
    '''
    :param chat_id: Telegram user chat_id.
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config.
    :param target_weekly_schedule_url: Url to the weekly target schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/.
    :return:
        Int - if any error was caused other than none schedule. Contains an error code that will be processed in
            processing_parser_errors function from utils/processing_parser_errors.
        Str - if the none schedule error was caused. Сontains the url to weekly schedule. This error is processed in
            processing_parser_none_schedule_error function from utils/processing_parser_none_schedule_error.
        Tuple - Contains a list with data for each day in the weekly schedule, a link to the weekly schedule and
            the names of columns to create schedule report.
    '''

    if target == STUDENT_TARGET:
        return await get_weekly_schedule_data(
            chat_id=chat_id,
            target=target,
            target_weekly_schedule_url=target_weekly_schedule_url,
            target_table_headers=STUDENT_TABLE_HEADERS
        )
    else:
        return await get_weekly_schedule_data(
            chat_id=chat_id,
            target=target,
            target_weekly_schedule_url=target_weekly_schedule_url,
            target_table_headers=LECTURER_TABLE_HEADERS
        )
