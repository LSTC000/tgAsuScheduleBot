from data.memory_storage import TARGET_KEY, SCHEDULE_INLINE_KEYBOARDS_KEY, INLINE_CALENDAR_KEY

from data.config import STUDENT_TARGET, LECTURER_TARGET, RATE_LIMIT_DICT, MENU_REPLAY_KEYBOARD_KEY

from data.messages import (
    ENTER_LECTURER_TARGET_NAME_MESSAGE,
    ENTER_STUDENT_TARGET_NAME_MESSAGE,
    STUDENT_TARGET_RKB_MESSAGE,
    LECTURER_TARGET_RKB_MESSAGE
)

from utils import rate_limit

from loader import dp, bot

from states import ScheduleMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(
    lambda m: m.text in [STUDENT_TARGET_RKB_MESSAGE, LECTURER_TARGET_RKB_MESSAGE],
    content_types=types.ContentType.TEXT,
    state=[ScheduleMenuStatesGroup.student_schedule, ScheduleMenuStatesGroup.lecturer_schedule]
)
@rate_limit(limit=RATE_LIMIT_DICT[MENU_REPLAY_KEYBOARD_KEY], key=MENU_REPLAY_KEYBOARD_KEY)
async def swap_schedule_target(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    text = message.text
    # Target is a STUDENT_TARGET, LECTURER_TARGET or a ROOM_TARGET in data/config/parsers/config.
    # Depending on which target the user chooses on the replay keyboard certain actions will be performed.
    if text == STUDENT_TARGET_RKB_MESSAGE:
        msg = ENTER_STUDENT_TARGET_NAME_MESSAGE

        async with state.proxy() as data:
            # Hiding all the schedule inline keyboards from the user for the last target if there are any.
            if data[SCHEDULE_INLINE_KEYBOARDS_KEY]:
                for message_id in data[SCHEDULE_INLINE_KEYBOARDS_KEY]:
                    await bot.edit_message_reply_markup(
                        chat_id=chat_id,
                        message_id=message_id,
                        reply_markup=None
                    )
            # Delete the last calendar inline keyboard if there is one.
            if data[INLINE_CALENDAR_KEY] is not None:
                await bot.delete_message(
                    chat_id=chat_id,
                    message_id=data[INLINE_CALENDAR_KEY]
                )
            # Clear all other data in the user's memory storage.
            data.clear()
            # Create variables in the user memory storage.
            data[TARGET_KEY] = STUDENT_TARGET
            data[SCHEDULE_INLINE_KEYBOARDS_KEY] = []
            data[INLINE_CALENDAR_KEY] = None

        await ScheduleMenuStatesGroup.student_schedule.set()
    else:
        msg = ENTER_LECTURER_TARGET_NAME_MESSAGE

        async with state.proxy() as data:
            # Hiding all the schedule inline keyboards from the user for the last target if there are any.
            if data[SCHEDULE_INLINE_KEYBOARDS_KEY]:
                for message_id in data[SCHEDULE_INLINE_KEYBOARDS_KEY]:
                    await bot.edit_message_reply_markup(
                        chat_id=chat_id,
                        message_id=message_id,
                        reply_markup=None
                    )
            # Delete the last calendar inline keyboard if there is one.
            if data[INLINE_CALENDAR_KEY] is not None:
                await bot.delete_message(
                    chat_id=chat_id,
                    message_id=data[INLINE_CALENDAR_KEY]
                )
            # Clear all other data in the user's memory storage.
            data.clear()
            # Create variables in the user memory storage.
            data[TARGET_KEY] = LECTURER_TARGET
            data[SCHEDULE_INLINE_KEYBOARDS_KEY] = []
            data[INLINE_CALENDAR_KEY] = None

        await ScheduleMenuStatesGroup.lecturer_schedule.set()

    await bot.send_message(chat_id=chat_id, text=msg)
