from typing import Union, List

from data.config import STUDENT_TARGET
from data.config import DAY_CONVERT_DICT
from data.config import ORDER_CONVERT_DICT

from utils.find_building_location_url_for_rooms import find_building_location_url_for_rooms


def create_report_weekly_schedule(
        target: str,
        target_schedule: Union[dict, list],
        target_name: str,
        target_url: str,
        target_table_headers: list
) -> List[str]:
    '''
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config
    :param target_schedule:
        Dict - Contains the key - the name of the table header and the value - the header data
        List - Contains a dictionary for each day in the weekly schedule, in which the key - the name of the table
            header and the value - the header data
    :param target_name: Alleged target name
    :param target_url: Url to the weekly target schedule.
        Example: https://www.asu.ru/timetable/students/21/2129440242/
    :param target_table_headers: STUDENT_TABLE_HEADERS or LECTURER_TABLE_HEADERS from data/config/parsers/config
    :return: List with daily schedule reports
    '''

    if target == STUDENT_TARGET:
        target = '👨‍🎓 Группа'
    else:
        target = '👩‍🏫 Преподаватель'
    # List with daily schedule reports
    report_list = [f'<b>{target}:</b> {target_name}']
    # Create a schedule report for each day of the week
    for daily_schedule in target_schedule:
        # Get the date from the daily_schedule
        day_date = daily_schedule[target_table_headers[0]].split()
        day = day_date[0]
        date = day_date[-1]
        # Daily schedule report header
        report = f'📌 <u><b>{DAY_CONVERT_DICT[day]}</b> {date}</u>\n\n'

        count_subjects = len(daily_schedule[target_table_headers[1]])
        # Create a daily schedule report
        for i in range(count_subjects):
            for key in target_table_headers[1:]:
                if key == target_table_headers[1]:
                    report += f'<b>{key}:</b> {ORDER_CONVERT_DICT[daily_schedule[key][i]]}\n'
                elif key == target_table_headers[-2]:
                    report += f'<b>{key}:</b> ' \
                              f'{find_building_location_url_for_rooms(daily_schedule[key][i])}\n'
                elif key == target_table_headers[-1]:
                    if daily_schedule[key][i]:
                        report += f'<a href="{daily_schedule[key][i]}" title="свободные аудитории"><b>{key}</b></a>\n'
                else:
                    report += f'<b>{key}:</b> {daily_schedule[key][i]}\n'
            report += '\n'
        # Add daily schedule report
        report_list.append(report)

    return report_list
