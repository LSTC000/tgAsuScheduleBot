from data.callbacks import CALLBACK_DATA_CONFIRM_CHAT_GPT_CLEAR_MESSAGES

from data.memory_storage import COUNT_CHAT_GPT_MESSAGES_KEY, CHAT_GPT_MESSAGES_KEY, LAST_CHAT_GPT_INLINE_KEYBOARD_KEY

from data.config import (
    RATE_LIMIT_DICT,
    MENU_REPLAY_KEYBOARD_KEY,
    CHAT_GPT_INLINE_KEYBOARD_KEY,
    CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE
)

from data.messages import (
    CLEAR_CHAT_GPT_MESSAGES_RKB_MESSAGE,
    CLEAR_CHAT_GPT_MESSAGES_MESSAGE,
    CONFIRM_CLEAR_CHAT_GPT_MESSAGES_MESSAGE,
    CANCEL_CLEAR_CHAT_GPT_MESSAGES_MESSAGE,
    EMPTY_CHAT_GPT_MESSAGES_MESSAGE
)

from keyboards import clear_chat_gpt_messages_ikb

from utils import rate_limit

from loader import dp, bot

from states import MenuStatesGroup, ChatGptMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(
    lambda m: m.text == CLEAR_CHAT_GPT_MESSAGES_RKB_MESSAGE,
    content_types=types.ContentType.TEXT,
    state=MenuStatesGroup.chat_gpt_menu
)
@rate_limit(limit=RATE_LIMIT_DICT[MENU_REPLAY_KEYBOARD_KEY], key=MENU_REPLAY_KEYBOARD_KEY)
async def clear_chat_gpt_messages(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        # If the user has Chat GPT messages, then we ask him for confirmation to delete them.
        # Else inform the user that his dialog with Chat GPT is empty.
        if data[COUNT_CHAT_GPT_MESSAGES_KEY]:
            message = await bot.send_message(
                chat_id=message.from_user.id,
                text=CLEAR_CHAT_GPT_MESSAGES_MESSAGE,
                reply_markup=clear_chat_gpt_messages_ikb()
            )
            # Assign an inline keyboard to confirm the deletion of the dialog with Chat GPT.
            data[LAST_CHAT_GPT_INLINE_KEYBOARD_KEY] = message.message_id
            await ChatGptMenuStatesGroup.chat_gpt_clear_messages.set()
        else:
            await bot.send_message(chat_id=message.from_user.id, text=EMPTY_CHAT_GPT_MESSAGES_MESSAGE)


@dp.callback_query_handler(state=ChatGptMenuStatesGroup.chat_gpt_clear_messages)
@rate_limit(limit=RATE_LIMIT_DICT[CHAT_GPT_INLINE_KEYBOARD_KEY], key=CHAT_GPT_INLINE_KEYBOARD_KEY)
async def confirm_clear_chat_gpt_messages(callback: types.CallbackQuery, state: FSMContext) -> None:
    # If the callback data contains confirmation of deleting the dialog then delete it.
    # Else we don't do anything.
    if callback.data == CALLBACK_DATA_CONFIRM_CHAT_GPT_CLEAR_MESSAGES:
        msg = CONFIRM_CLEAR_CHAT_GPT_MESSAGES_MESSAGE.format(callback.from_user.first_name)
        # Reset user messages data for Chat GPT.
        async with state.proxy() as data:
            data[CHAT_GPT_MESSAGES_KEY].clear()
            data[CHAT_GPT_MESSAGES_KEY].append(CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE)
            data[COUNT_CHAT_GPT_MESSAGES_KEY] = 0
    else:
        msg = CANCEL_CLEAR_CHAT_GPT_MESSAGES_MESSAGE

    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=msg)
    await MenuStatesGroup.chat_gpt_menu.set()
