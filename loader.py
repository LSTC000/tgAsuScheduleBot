import logging

from data.config import (
    BOT_TOKEN,
    PARSE_MODE,
    DISABLE_WEB_PAGE_PREVIEW,
    STT_LOW_MODEL_PATH,
    STT_HIGH_MODEL_PATH,
    SAMPLE_RATE,
    FFMPEG_PATH,
    SCHEDULE_MAXSIZE,
    VOICE_MAXSIZE,
    SCHEDULE_TTL,
    VOICE_TTL,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB
)

from stt import STT

from gino import Gino

from cachetools import TTLCache

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2


__all__ = ['bot', 'dp', 'schedule_stt', 'chat_gpt_stt', 'db', 'schedule_cache', 'voice_cache', 'logger']


storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

bot = Bot(token=BOT_TOKEN, parse_mode=PARSE_MODE, disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW)
dp = Dispatcher(bot=bot, storage=storage)

schedule_stt = STT(model_path=STT_LOW_MODEL_PATH, sample_rate=SAMPLE_RATE, ffmpeg_path=FFMPEG_PATH)
chat_gpt_stt = STT(model_path=STT_LOW_MODEL_PATH, sample_rate=SAMPLE_RATE, ffmpeg_path=FFMPEG_PATH)

db = Gino()

schedule_cache = TTLCache(maxsize=SCHEDULE_MAXSIZE, ttl=SCHEDULE_TTL)
voice_cache = TTLCache(maxsize=VOICE_MAXSIZE, ttl=VOICE_TTL)

logger = logging.getLogger(__name__)
