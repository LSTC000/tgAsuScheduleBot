import logging

from data.config import SKIP_UPDATES, ADMIN

from loader import dp, bot, logger

from database import startup_setup, shutdown_setup

from middlewares import ThrottlingAndDatabaseMiddleware

from handlers import (
    register_users_commands,
    set_default_commands,
    register_users_cancels,
    register_users_main_menu,
    register_users_invalid_messages,
    register_users_schedule_menu,
    register_users_chat_gpt_menu
)

from aiogram import Bot, Dispatcher
from aiogram.utils import executor


def register_all_handlers(dispatcher: Dispatcher):
    register_users_cancels(dispatcher)
    register_users_main_menu(dispatcher)
    register_users_schedule_menu(dispatcher)
    register_users_chat_gpt_menu(dispatcher)
    register_users_invalid_messages(dispatcher)
    register_users_commands(dispatcher)


def register_all_middlewares(dispatcher: Dispatcher):
    dispatcher.setup_middleware(ThrottlingAndDatabaseMiddleware())


async def set_all_default_commands(_bot: Bot):
    await set_default_commands(_bot)


async def on_startup(dispatcher: Dispatcher):
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot!')
    await bot.send_message(chat_id=ADMIN, text='Starting bot!')

    logger.info('Setup PostgreSQL Connection')
    await startup_setup()

    logger.info('Register all middlewares')
    register_all_middlewares(dispatcher)

    logger.info('Set all default commands')
    await set_all_default_commands(bot)

    logger.info('Register all handlers')
    register_all_handlers(dispatcher)


async def on_shutdown(dispatcher: Dispatcher):
    logger.info('Closing PostgreSQL Connection')
    await shutdown_setup()

    logger.info('Bot successfully stopped!')
    await bot.send_message(chat_id=ADMIN, text='Bot successfully stopped!')


if __name__ == '__main__':
    try:
        executor.start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=SKIP_UPDATES
        )
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
        raise
