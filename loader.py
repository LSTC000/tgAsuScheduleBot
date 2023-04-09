import logging

from data.config import BOT_TOKEN
from data.config import PARSE_MODE
from data.config import DISABLE_WEB_PAGE_PREVIEW
from data.config import STT_LOW_MODEL_PATH
from data.config import STT_HIGH_MODEL_PATH
from data.config import SAMPLE_RATE
from data.config import FFMPEG_PATH
from data.config import SCHEDULE_MAXSIZE, VOICE_MAXSIZE
from data.config import SCHEDULE_TTL, VOICE_TTL

from stt import STT

from gino import Gino

from cachetools import TTLCache

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


__all__ = ['bot', 'dp', 'schedule_stt', 'chat_gpt_stt', 'db', 'schedule_cache', 'voice_cache', 'logger']


storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode=PARSE_MODE, disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW)
dp = Dispatcher(bot=bot, storage=storage)

schedule_stt = STT(model_path=STT_LOW_MODEL_PATH, sample_rate=SAMPLE_RATE, ffmpeg_path=FFMPEG_PATH)
chat_gpt_stt = STT(model_path=STT_LOW_MODEL_PATH, sample_rate=SAMPLE_RATE, ffmpeg_path=FFMPEG_PATH)

db = Gino()

schedule_cache = TTLCache(maxsize=SCHEDULE_MAXSIZE, ttl=SCHEDULE_TTL)
voice_cache = TTLCache(maxsize=VOICE_MAXSIZE, ttl=VOICE_TTL)

logger = logging.getLogger(__name__)
