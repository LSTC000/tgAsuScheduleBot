from database.database_setup import TimedBaseModel

from sqlalchemy import Column, BigInteger, VARCHAR, sql


class UsersMessages(TimedBaseModel):
    __tablename__ = 'users_messages'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'users_messages_id_seq\')'))
    # Telegram user_id.
    user_id = Column(BigInteger, nullable=False)
    # Type of message: voice or text.
    message_type = Column(VARCHAR(8), nullable=False)
    # Any message keys from data/config/middlewares/config except CHAT_GPT_MESSAGE_KEY.
    message_key = Column(VARCHAR(32), nullable=False)

    query: sql.select
