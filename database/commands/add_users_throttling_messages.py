from loader import logger

from asyncpg import UniqueViolationError

from database import UsersThrottlingMessages


async def add_users_throttling_messages(user_id: int, throttling_key: str, sleep_time: int) -> None:
    '''
    :param user_id: Telegram user_id
    :param throttling_key: Any key from data/config/middlewares/config
    :param sleep_time: Throttling sleep time
    :return: None
    '''

    try:
        user_throttling_message = UsersThrottlingMessages(
            user_id=user_id,
            throttling_key=throttling_key,
            sleep_time=sleep_time
        )

        # Create a new record in the UsersThrottlingMessages table for the user, indicating that they have triggered a
        # throttling message with the specified key and should wait for the specified time before sending another message
        # The create() method is a method of the UsersMessages model, which is responsible for interacting with the database
        await user_throttling_message.create()

    except UniqueViolationError:
        logger.info('Error to add user throttling message! User throttling message already exists in the database.')
