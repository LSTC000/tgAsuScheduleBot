from data.config import RATE_LIMIT_DICT
from data.config import SCHEDULE_MESSAGE_KEY
from data.config import STUDENT_TARGET, LECTURER_TARGET

from data.messages import VOICE_CONVERT_ERROR_MESSAGE
from data.messages import CALLBACK_DATA_KEY_ERROR_MESSAGE

from functions import get_daily_schedule
from functions import voice_to_text_convert

from utils import rate_limit
from utils import get_date_query_url_codes

from ner import text_to_student_group_convert
from ner import find_lecturer_name_in_text

from loader import dp, bot, schedule_stt
from states import ScheduleMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound


@dp.message_handler(
    content_types=[types.ContentType.TEXT, types.ContentType.VOICE],
    state=[ScheduleMenuStatesGroup.student_schedule, ScheduleMenuStatesGroup.lecturer_schedule]
)
@rate_limit(limit=RATE_LIMIT_DICT[SCHEDULE_MESSAGE_KEY], key=SCHEDULE_MESSAGE_KEY)
async def get_today_schedule(message: types.Message, state: FSMContext) -> None:
    # Flag for checking the KeyError in process voice message
    key_error = False
    # If the message is voice then we process it
    if message.content_type == 'voice':
        alleged_target_name = await voice_to_text_convert(
            user_id=message.from_user.id,
            file_id=message.voice.file_id,
            stt=schedule_stt
        )
        # If the target is a student target then it is necessary to convert the text to a number
        # If the target is a lecturer then it is necessary to find his surname first name and patronymic in the context
        async with state.proxy() as data:
            if alleged_target_name is not None:
                try:
                    if data['target'] == STUDENT_TARGET:
                        alleged_target_name = await text_to_student_group_convert(
                            text=alleged_target_name,
                            target=STUDENT_TARGET
                        )
                    else:
                        if len(alleged_target_name.split()) == 1:
                            alleged_target_name = await find_lecturer_name_in_text(
                                text=alleged_target_name,
                                target=LECTURER_TARGET,
                                only_last_name=True
                            )
                        else:
                            alleged_target_name = await find_lecturer_name_in_text(
                                text=alleged_target_name,
                                target=LECTURER_TARGET,
                                only_last_name=False
                            )
                except KeyError:
                    alleged_target_name = None
                    key_error = True
                    await bot.send_message(chat_id=message.from_user.id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)
    else:
        alleged_target_name = message.text
    # If we were unable to process the voice message then we send a message about it
    if alleged_target_name is None:
        if not key_error:
            await bot.send_message(chat_id=message.from_user.id, text=VOICE_CONVERT_ERROR_MESSAGE)
    else:
        # Find date query url codes in format %Y%m%d without separation for finding the schedule for today and tomorrow
        today_target_date_query_url_code, tomorrow_target_date_query_url_code = get_date_query_url_codes()

        try:
            async with state.proxy() as data:
                # Hiding all the schedule inline keyboards from the user for the last target if there are any
                if data['message_id_last_schedule_inline_keyboards']:
                    for message_id in data['message_id_last_schedule_inline_keyboards']:
                        try:
                            await bot.edit_message_reply_markup(
                                chat_id=message.chat.id,
                                message_id=message_id,
                                reply_markup=None
                            )
                        except MessageNotModified:
                            pass
                    data['message_id_last_schedule_inline_keyboards'].clear()
                # Delete the last calendar inline keyboard if there is one
                if data['calendar_message_id'] is not None:
                    try:
                        await bot.delete_message(
                            chat_id=message.chat.id,
                            message_id=data['calendar_message_id']
                        )
                    except MessageToDeleteNotFound:
                        pass
                    data['calendar_message_id'] = None

                '''Create variables in the user memory storage'''
                # target_url: Url to the weekly target schedule. From it you can get an url to the schedule
                # of a certain day, if you add to its end DATE_QUERY_URL from data/urls/urls.
                # Until we called the function get_daily_schedule equals None
                data['target_url'] = None
                # alleged_target_name: This is the alleged name of the target because at the beginning we cannot say
                # the exact name of the target, since the user can enter an incomplete name of the target and
                # then the bot will offer him a choice on the inline keyboard
                data['alleged_target_name'] = alleged_target_name
                # today_target_date_query_url_code: Today date in format %Y%m%d without separation
                data['today_target_date_query_url_code'] = today_target_date_query_url_code
                # tomorrow_target_date_query_url_code: Tomorrow date in format %Y%m%d without separation
                data['tomorrow_target_date_query_url_code'] = tomorrow_target_date_query_url_code
                # target_date_query_url_code: Url code for finding a schedule for today, tomorrow or a calendar
                # schedule. We don't use for finding schedules today_target_date_query_url_code or
                # tomorrow_target_date_query_url_code because these variables are only needed to store today and
                # tomorrow date
                data['target_date_query_url_code'] = data['today_target_date_query_url_code']

            # Get daily schedule: check functions/get_daily_schedule
            # The schedule_cache check is in this function
            await get_daily_schedule(
                chat_id=message.from_user.id,
                user_name=message.from_user.first_name,
                daily=True,
                today=True,
                calendar=False,
                state=state
            )
        except KeyError:
            await bot.send_message(chat_id=message.from_user.id, text=CALLBACK_DATA_KEY_ERROR_MESSAGE)
