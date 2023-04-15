import os

from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(find_dotenv())

CHAT_GPT_TOKEN = os.getenv('CHAT_GPT_TOKEN')

MODEL = "gpt-3.5-turbo"
MAX_CONTENT_TOKENS = 3000
MAX_TOKENS = 4096
TEMPERATURE = 0.5
MAX_CHAT_GPT_MESSAGES = 25

CHAT_GPT_ROLE = "assistant"
CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE = {'role': 'assistant', 'content': 'You’re a kind helpful assistant'}
