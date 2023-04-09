from data.config import RATE_LIMIT_DICT
from data.config import MENU_REPLAY_KEYBOARD_KEY

from data.messages import MAIN_MENU_COMMAND_MESSAGE
from data.messages import CANCEL_TO_MAIN_MENU_RKB_BUTTON_MESSAGE

from keyboards import get_main_menu_rkb

from utils import rate_limit

from loader import dp, bot
from states import MenuStatesGroup, ScheduleMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound


@dp.message_handler(
    lambda m: m.text == CANCEL_TO_MAIN_MENU_RKB_BUTTON_MESSAGE,
    content_types=types.ContentType.TEXT,
    state=[
        MenuStatesGroup.schedule_menu,
        ScheduleMenuStatesGroup.student_schedule,
        ScheduleMenuStatesGroup.lecturer_schedule
    ]
)
@rate_limit(limit=RATE_LIMIT_DICT[MENU_REPLAY_KEYBOARD_KEY], key=MENU_REPLAY_KEYBOARD_KEY)
async def cancel_to_main_menu_from_schedule_menu(message: types.Message, state: FSMContext) -> None:
    msg = MAIN_MENU_COMMAND_MESSAGE
    main_menu_rkb = get_main_menu_rkb()
    current_state = await state.get_state()
    # Clear all user data in memory storage
    if current_state in [
        ScheduleMenuStatesGroup.lecturer_schedule.state,
        ScheduleMenuStatesGroup.student_schedule.state
    ]:
        async with state.proxy() as data:
            try:
                # Hiding all the schedule inline keyboards from the user for the last target if there are any
                if data['message_id_last_schedule_inline_keyboards']:
                    for message_id in data['message_id_last_schedule_inline_keyboards']:
                        try:
                            await bot.edit_message_reply_markup(
                                chat_id=message.chat.id,
                                message_id=message_id,
                                reply_markup=None
                            )
                        except (MessageNotModified, MessageToEditNotFound):
                            pass
                # Delete the last calendar inline keyboard if there is one
                if data['calendar_message_id'] is not None:
                    try:
                        await bot.delete_message(
                            chat_id=message.chat.id,
                            message_id=data['calendar_message_id']
                        )
                    except MessageToDeleteNotFound:
                        pass
                data.clear()
            except KeyError:
                data.clear()
    else:
        async with state.proxy() as data:
            data.clear()

    await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=main_menu_rkb)
    await MenuStatesGroup.main_menu.set()
