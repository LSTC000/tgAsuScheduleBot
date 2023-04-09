from loader import logger

from asyncpg import UniqueViolationError

from database import UsersMessages


async def add_users_messages(user_id: int, message_type: str, message_key: str) -> None:
    '''
    :param user_id: Telegram user_id
    :param message_type: Text or voice message type
    :param message_key: Any message keys from data/config/middlewares/config except CHAT_GPT_MESSAGE_KEY
    :return: None
    '''

    try:
        user_message = UsersMessages(user_id=user_id, message_type=message_type, message_key=message_key)

        # Create a new user message in the database using the provided user_id, message and message_key
        # The create() method is a method of the UsersMessages model, which is responsible for interacting with the database
        await user_message.create()

    except UniqueViolationError:
        logger.info('Error to add user message! User message already exists in the database.')
