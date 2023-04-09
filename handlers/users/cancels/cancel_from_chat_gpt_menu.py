from data.config import RATE_LIMIT_DICT
from data.config import MENU_REPLAY_KEYBOARD_KEY
from data.config import CHAT_GPT_INLINE_KEYBOARD_KEY
from data.config import CALLBACK_DATA_CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU

from data.messages import MAIN_MENU_COMMAND_MESSAGE
from data.messages import CANCEL_TO_MAIN_MENU_RKB_BUTTON_MESSAGE
from data.messages import CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE
from data.messages import CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE
from data.messages import CANCEL_CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE

from keyboards import get_main_menu_rkb, chat_gpt_return_to_main_menu_ikb

from utils import rate_limit

from loader import dp, bot
from states import MenuStatesGroup, ChatGptMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(
    lambda m: m.text == CANCEL_TO_MAIN_MENU_RKB_BUTTON_MESSAGE,
    content_types=types.ContentType.TEXT,
    state=[MenuStatesGroup.chat_gpt_menu, ChatGptMenuStatesGroup.chat_gpt_clear_messages]
)
@rate_limit(limit=RATE_LIMIT_DICT[MENU_REPLAY_KEYBOARD_KEY], key=MENU_REPLAY_KEYBOARD_KEY)
async def cancel_to_main_menu_from_chat_gpt_menu(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == ChatGptMenuStatesGroup.chat_gpt_clear_messages.state:
        # Delete last Chat GPT inline keyboard
        # In this case, it will be an inline keyboard about clearing the history of the dialog with Chat GPT
        # And we have to replace this inline keyboard with an inline keyboard confirming the transition to the main menu
        async with state.proxy() as data:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=data['message_id_last_chat_gpt_inline_keyboard']
            )

            msg = CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE
            ikb = chat_gpt_return_to_main_menu_ikb()

            message = await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=ikb)
            # Here it would be possible not to remember the last inline keyboard id because in the
            # confirm_chat_gpt_cancel_to_main_menu, we will not use data['message_id_last_chat_gpt_inline_keyboard'],
            # but we will use callback.message.message_id, but we will need to store this last inline keyboard id
            # so that when the user calls the /start command in the confirm_clear_chat_gpt inline keyboard, we have
            # access to it to delete it, since the command /start displays a welcome message and
            # takes us to the main menu. Check command /start in handlers/users/commands/start
            data['message_id_last_chat_gpt_inline_keyboard'] = message.message_id

        await ChatGptMenuStatesGroup.chat_gpt_confirm_cancel_to_main_menu.set()
    else:
        # Flag is True if the user did not send Chat GPT messages
        # else False and we must request confirmation of the exit to the main menu
        flag = False

        async with state.proxy() as data:
            if data['count_chat_gpt_messages']:
                flag = True

                msg = CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE
                ikb = chat_gpt_return_to_main_menu_ikb()

                await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=ikb)
            else:
                msg = MAIN_MENU_COMMAND_MESSAGE
                main_menu_rkb = get_main_menu_rkb()
                data.clear()

                await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=main_menu_rkb)

        if flag:
            await ChatGptMenuStatesGroup.chat_gpt_confirm_cancel_to_main_menu.set()
        else:
            await MenuStatesGroup.main_menu.set()


@dp.callback_query_handler(state=ChatGptMenuStatesGroup.chat_gpt_confirm_cancel_to_main_menu)
@rate_limit(limit=RATE_LIMIT_DICT[CHAT_GPT_INLINE_KEYBOARD_KEY], key=CHAT_GPT_INLINE_KEYBOARD_KEY)
async def confirm_chat_gpt_cancel_to_main_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    # If the callback data contains confirmation of entering the main menu
    # Else we remain in the Chat GPT menu
    if callback.data == CALLBACK_DATA_CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU:
        msg = CONFIRM_CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE.format(callback.from_user.first_name)
        # Inform the user that his dialog with Chat GPT has been deleted
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=msg
        )
        # Clear all user data in memory storage
        async with state.proxy() as data:
            data.clear()

        msg = MAIN_MENU_COMMAND_MESSAGE
        main_menu_rkb = get_main_menu_rkb()

        await bot.send_message(chat_id=callback.from_user.id, text=msg, reply_markup=main_menu_rkb)
        await MenuStatesGroup.main_menu.set()
    else:
        msg = CANCEL_CHAT_GPT_CANCEL_TO_MAIN_MENU_MESSAGE.format(callback.from_user.first_name)
        # Inform the user that he can continue the dialogue with Chat GPT
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=msg
        )

        await MenuStatesGroup.chat_gpt_menu.set()
