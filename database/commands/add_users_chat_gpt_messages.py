from loader import logger

from asyncpg import UniqueViolationError

from database import UsersChatGptMessages


async def add_users_chat_gpt_messages(user_id: int, message_type: str) -> None:
    '''
    :param user_id: Telegram user id.
    :param message_type: Text or voice message type.
    :return: None.
    '''

    try:
        user_chat_gpt_message = UsersChatGptMessages(user_id=user_id, message_type=message_type)

        # Create a new user chat GPT message in the database using the provided user_id and message.
        # The create() method is a method of the UsersChatGptMessages model,
        # which is responsible for interacting with the database.
        await user_chat_gpt_message.create()

    except UniqueViolationError:
        logger.info('Error to add user chat gpt message! User chat gpt message already exists in the database.')
