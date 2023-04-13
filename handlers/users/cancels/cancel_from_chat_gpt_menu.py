from data.callbacks import CALLBACK_DATA_CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU

from data.memory_storage import COUNT_CHAT_GPT_MESSAGES_KEY, LAST_CHAT_GPT_INLINE_KEYBOARD_KEY

from data.config import RATE_LIMIT_DICT, MENU_REPLAY_KEYBOARD_KEY, CHAT_GPT_INLINE_KEYBOARD_KEY

from data.messages import (
    MAIN_MENU_COMMAND_MESSAGE,
    CANCEL_TO_MAIN_MENU_RKB_MESSAGE,
    CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE,
    CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE,
    CANCEL_CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE
)

from keyboards import get_main_menu_rkb, chat_gpt_return_to_main_menu_ikb

from utils import rate_limit

from loader import dp, bot
from states import MenuStatesGroup, ChatGptMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(
    lambda m: m.text == CANCEL_TO_MAIN_MENU_RKB_MESSAGE,
    content_types=types.ContentType.TEXT,
    state=[MenuStatesGroup.chat_gpt_menu, ChatGptMenuStatesGroup.chat_gpt_clear_messages]
)
@rate_limit(limit=RATE_LIMIT_DICT[MENU_REPLAY_KEYBOARD_KEY], key=MENU_REPLAY_KEYBOARD_KEY)
async def cancel_to_main_menu_from_chat_gpt_menu(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    current_state = await state.get_state()

    if current_state == ChatGptMenuStatesGroup.chat_gpt_clear_messages.state:
        # Delete last Chat GPT inline keyboard.
        # In this case, it will be an inline keyboard about clearing the history of the dialog with Chat GPT.
        # And we have to replace this inline keyboard with an inline keyboard confirming the transition to the main
        # menu.
        async with state.proxy() as data:
            await bot.delete_message(
                chat_id=chat_id,
                message_id=data[LAST_CHAT_GPT_INLINE_KEYBOARD_KEY]
            )

            message = await bot.send_message(
                chat_id=chat_id,
                text=CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE,
                reply_markup=chat_gpt_return_to_main_menu_ikb()
            )
            # Here it would be possible not to remember the last inline keyboard id because in the
            # confirm_chat_gpt_cancel_to_main_menu, we will not use data[LAST_CHAT_GPT_INLINE_KEYBOARD_KEY],
            # but we will use callback.message.message_id, but we will need to store this last inline keyboard id
            # so that when the user calls the /start command in the confirm_clear_chat_gpt inline keyboard, we have
            # access to it to delete it, since the command /start displays a welcome message and
            # takes us to the main menu. Check command /start in handlers/users/commands/start.
            data[LAST_CHAT_GPT_INLINE_KEYBOARD_KEY] = message.message_id

        await ChatGptMenuStatesGroup.chat_gpt_confirm_cancel_to_main_menu.set()
    else:
        # Flag is True if the user did not send Chat GPT messages else False and we must request confirmation
        # of the exit to the main menu.
        flag = False

        async with state.proxy() as data:
            if data[COUNT_CHAT_GPT_MESSAGES_KEY]:
                flag = True
                await bot.send_message(
                    chat_id=chat_id,
                    text=CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE,
                    reply_markup=chat_gpt_return_to_main_menu_ikb()
                )
            else:
                data.clear()
                await bot.send_message(
                    chat_id=chat_id,
                    text=MAIN_MENU_COMMAND_MESSAGE,
                    reply_markup=get_main_menu_rkb()
                )

        if flag:
            await ChatGptMenuStatesGroup.chat_gpt_confirm_cancel_to_main_menu.set()
        else:
            await MenuStatesGroup.main_menu.set()


@dp.callback_query_handler(state=ChatGptMenuStatesGroup.chat_gpt_confirm_cancel_to_main_menu)
@rate_limit(limit=RATE_LIMIT_DICT[CHAT_GPT_INLINE_KEYBOARD_KEY], key=CHAT_GPT_INLINE_KEYBOARD_KEY)
async def confirm_chat_gpt_cancel_to_main_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    # If the callback data contains confirmation of entering the main menu.
    # Else we remain in the Chat GPT menu.
    if callback.data == CALLBACK_DATA_CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU:
        # Inform the user that his dialog with Chat GPT has been deleted.
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.message_id,
            text=CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE.format(callback.from_user.first_name)
        )
        # Clear all user data in memory storage.
        async with state.proxy() as data:
            data.clear()

        await bot.send_message(
            chat_id=chat_id,
            text=MAIN_MENU_COMMAND_MESSAGE,
            reply_markup=get_main_menu_rkb()
        )
        await MenuStatesGroup.main_menu.set()
    else:
        # Inform the user that he can continue the dialogue with Chat GPT.
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.message_id,
            text=CANCEL_CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE.format(callback.from_user.first_name)
        )
        await MenuStatesGroup.chat_gpt_menu.set()
