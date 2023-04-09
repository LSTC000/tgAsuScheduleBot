from data.config import RATE_LIMIT_DICT
from data.config import CHAT_GPT_MESSAGE_KEY
from data.config import CHAT_GPT_TOKEN
from data.config import MODEL
from data.config import MAX_TOKENS
from data.config import TEMPERATURE
from data.config import MAX_CHAT_GPT_MESSAGES
from data.config import CHAT_GPT_ROLE
from data.config import CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE

from data.messages import START_FIND_CHAT_GPT_MESSAGE
from data.messages import VOICE_CONVERT_ERROR_MESSAGE
from data.messages import LIMIT_CHAT_GPT_MESSAGES_MESSAGE
from data.messages import CHAT_GPT_CONNECT_ERROR_MESSAGE

from functions import voice_to_text_convert

from utils import rate_limit

from loader import dp, bot, chat_gpt_stt

from states import MenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext

import openai
from openai.error import Timeout


openai.api_key = CHAT_GPT_TOKEN


@dp.message_handler(
    content_types=[types.ContentType.TEXT, types.ContentType.VOICE],
    state=MenuStatesGroup.chat_gpt_menu
)
@rate_limit(limit=RATE_LIMIT_DICT[CHAT_GPT_MESSAGE_KEY], key=CHAT_GPT_MESSAGE_KEY)
async def chat_gpt_response(message: types.Message, state: FSMContext) -> None:
    # If the message is voice then we process it
    if message.content_type == 'voice':
        content = await voice_to_text_convert(
            user_id=message.from_user.id,
            file_id=message.voice.file_id,
            stt=chat_gpt_stt
        )
    else:
        content = message.text
    # If we were unable to process the voice message then we send a message about it
    if content is None:
        await bot.send_message(chat_id=message.from_user.id, text=VOICE_CONVERT_ERROR_MESSAGE)
    else:
        start_find_message = await bot.send_message(chat_id=message.from_user.id, text=START_FIND_CHAT_GPT_MESSAGE)

        async with state.proxy() as data:
            try:
                # Add the user message to the history of the Chat GPT dialog
                data['chat_gpt_messages'].append({"role": "user", "content": content})
                data['count_chat_gpt_messages'] += 1
                # Send a request to receive a response from Chat GPT
                response = await openai.ChatCompletion.acreate(
                    model=MODEL,
                    messages=data['chat_gpt_messages'],
                    temperature=TEMPERATURE
                )
                # If the response from Chat GPT has arrived then add it to the history of the dialog
                # And assign a message counter to the response
                model_content = response['choices'][0]['message']['content']
                data['chat_gpt_messages'].append({"role": CHAT_GPT_ROLE, "content": model_content})
                model_content = f"<b>{data['count_chat_gpt_messages']}/{MAX_CHAT_GPT_MESSAGES}:</b> " + model_content
                # Counting tokens
                count_tokens = len(model_content)
                # If the number of tokens is greater than the MAX_TOKENS
                # Then we split the response from Chat GPT into several parts
                if count_tokens > MAX_TOKENS:
                    for i in range(0, count_tokens, MAX_TOKENS):
                        if count_tokens - i > MAX_TOKENS:
                            text = model_content[i:(MAX_TOKENS * (i + 1))]
                            await bot.send_message(chat_id=message.from_user.id, text=text)
                        else:
                            text = model_content[i:count_tokens]
                            await bot.send_message(chat_id=message.from_user.id, text=text)
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=model_content)
                # If the message limit for one dialog with Chat GPT is reached
                # Then we clear it and send a message to the user about it
                if data['count_chat_gpt_messages'] == MAX_CHAT_GPT_MESSAGES:
                    data['chat_gpt_messages'].clear()
                    data['chat_gpt_messages'].append(CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE)
                    data['count_chat_gpt_messages'] = 0

                    msg = LIMIT_CHAT_GPT_MESSAGES_MESSAGE.format(MAX_CHAT_GPT_MESSAGES)
                    await bot.send_message(chat_id=message.from_user.id, text=msg)
            except (KeyError, Timeout):
                await message.reply(text=CHAT_GPT_CONNECT_ERROR_MESSAGE)

        await bot.delete_message(chat_id=message.chat.id, message_id=start_find_message.message_id)