from data.config import STUDENT_TARGET, LECTURER_TARGET, RATE_LIMIT_DICT, MENU_REPLAY_KEYBOARD_KEY

from data.messages import (
    ENTER_LECTURER_TARGET_NAME_MESSAGE,
    ENTER_STUDENT_TARGET_NAME_MESSAGE,
    STUDENT_TARGET_RKB_MESSAGE,
    LECTURER_TARGET_RKB_MESSAGE
)

from utils import rate_limit

from loader import dp, bot

from states import MenuStatesGroup, ScheduleMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(
    lambda m: m.text in [STUDENT_TARGET_RKB_MESSAGE, LECTURER_TARGET_RKB_MESSAGE],
    content_types=types.ContentType.TEXT,
    state=MenuStatesGroup.schedule_menu
)
@rate_limit(limit=RATE_LIMIT_DICT[MENU_REPLAY_KEYBOARD_KEY], key=MENU_REPLAY_KEYBOARD_KEY)
async def first_choice_schedule_target(message: types.Message, state: FSMContext) -> None:
    text = message.text
    # Target is a STUDENT_TARGET or a LECTURER_TARGET in data/config/parsers/config.
    # Depending on which target the user chooses on the replay keyboard certain actions will be performed.
    if text == STUDENT_TARGET_RKB_MESSAGE:
        msg = ENTER_STUDENT_TARGET_NAME_MESSAGE
        # Create variables in the user memory storage.
        async with state.proxy() as data:
            data['target'] = STUDENT_TARGET
            data['message_id_last_schedule_inline_keyboards'] = []
            data['calendar_message_id'] = None

        await ScheduleMenuStatesGroup.student_schedule.set()
    else:
        msg = ENTER_LECTURER_TARGET_NAME_MESSAGE
        # Create variables in the user memory storage.
        async with state.proxy() as data:
            data['target'] = LECTURER_TARGET
            data['message_id_last_schedule_inline_keyboards'] = []
            data['calendar_message_id'] = None

        await ScheduleMenuStatesGroup.lecturer_schedule.set()

    await bot.send_message(chat_id=message.from_user.id, text=msg)
