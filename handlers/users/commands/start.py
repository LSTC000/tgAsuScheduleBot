from data.config import RATE_LIMIT_DICT
from data.config import COMMAND_KEY

from data.messages import START_COMMAND_MESSAGE
from data.messages import MAIN_MENU_COMMAND_MESSAGE

from keyboards import get_main_menu_rkb

from loader import dp, bot
from states import MenuStatesGroup, ScheduleMenuStatesGroup, ChatGptMenuStatesGroup

from utils import rate_limit

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToEditNotFound


@dp.message_handler(commands=['start'], state='*')
@rate_limit(limit=RATE_LIMIT_DICT[COMMAND_KEY], key=COMMAND_KEY)
async def start_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    # Clear all user data in memory storage
    if current_state in [ScheduleMenuStatesGroup.lecturer_schedule.state, ScheduleMenuStatesGroup.student_schedule.state]:
        async with state.proxy() as data:
            try:
                # Hiding all the schedule inline keyboards from the user for the last target if there are any
                if data['message_id_last_schedule_inline_keyboards']:
                    for message_id in data['message_id_last_schedule_inline_keyboards']:
                        await bot.edit_message_reply_markup(
                            chat_id=message.chat.id,
                            message_id=message_id,
                            reply_markup=None
                        )
                # Delete the last calendar inline keyboard if there is one
                if data['calendar_message_id'] is not None:
                    await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=data['calendar_message_id']
                    )

                data.clear()
            except (KeyError, MessageToEditNotFound):
                data.clear()
    # Clear all user data in memory storage
    if current_state == MenuStatesGroup.chat_gpt_menu.state:
        async with state.proxy() as data:
            data.clear()
    # Clear all user data in memory storage
    if current_state in [ChatGptMenuStatesGroup.chat_gpt_clear_messages.state, ChatGptMenuStatesGroup.chat_gpt_confirm_cancel_to_main_menu.state]:
        # Delete last Chat GPT inline keyboard
        async with state.proxy() as data:
            try:
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=data['message_id_last_chat_gpt_inline_keyboard']
                )
                data.clear()
            except KeyError:
                data.clear()
    # Calling a welcome message and going to the main menu
    msg = START_COMMAND_MESSAGE.format(message.from_user.first_name)
    mode_rkb = get_main_menu_rkb()
    await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=mode_rkb)

    msg = MAIN_MENU_COMMAND_MESSAGE
    await bot.send_message(chat_id=message.from_user.id, text=msg)

    await MenuStatesGroup.main_menu.set()
