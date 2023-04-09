from data.config import STUDENT_TARGET, LECTURER_TARGET

from data.urls import SCHEDULE_ASU_URL

from errors import GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_CODE
from data.messages import GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_STUDENT_MESSAGE
from data.messages import GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_LECTURER_MESSAGE

from errors import GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_CODE
from data.messages import GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_STUDENT_MESSAGE
from data.messages import GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_LECTURER_MESSAGE

from errors import GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_CODE
from data.messages import GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_STUDENT_MESSAGE
from data.messages import GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_LECTURER_MESSAGE

from errors import GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_CODE
from data.messages import GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_STUDENT_MESSAGE
from data.messages import GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_LECTURER_MESSAGE

from errors import GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_CODE
from data.messages import GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_STUDENT_MESSAGE
from data.messages import GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_LECTURER_MESSAGE


def processing_parser_errors(
        error_code: int,
        user_name: str,
        target: str
) -> str:
    '''
    :param error_code: Error code from errors/daily_schedule_parser or errors/weekly_schedule_parser
    :param user_name: Telegram user first name
    :param target: STUDENT_TARGET or LECTURER_TARGET from data/config/parser/config
    :return: Error message
    '''

    if target == STUDENT_TARGET:
        if error_code == GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_CODE:
            return GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_STUDENT_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        elif error_code == GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_CODE:
            return GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_STUDENT_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        elif error_code == GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_CODE:
            return GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_STUDENT_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        elif error_code == GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_CODE:
            return GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_STUDENT_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        elif error_code == GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_CODE:
            return GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_STUDENT_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        else:
            return ''
    else:
        if error_code == GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_CODE:
            return GET_ALLEGED_TARGETS_URLS_DICT_RESPONSE_OR_JSON_ERROR_LECTURER_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        elif error_code == GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_CODE:
            return GET_ALLEGED_TARGETS_URLS_DICT_NONE_TARGET_NAME_ERROR_LECTURER_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        elif error_code == GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_CODE:
            return GET_ALLEGED_TARGETS_URLS_DICT_COUNT_SHOW_ALLEGED_TARGET_NAMES_THRESHOLD_ERROR_LECTURER_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        elif error_code == GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_CODE:
            return GET_DAILY_SCHEDULE_DICT_RESPONSE_OR_JSON_ERROR_LECTURER_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        elif error_code == GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_CODE:
            return GET_WEEKLY_SCHEDULE_LIST_RESPONSE_OR_JSON_ERROR_LECTURER_MESSAGE.format(
                user_name,
                SCHEDULE_ASU_URL
            )
        else:
            return ''
