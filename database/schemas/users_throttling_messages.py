from database.database_setup import TimedBaseModel

from sqlalchemy import Column, BigInteger, Integer, VARCHAR, sql


class UsersThrottlingMessages(TimedBaseModel):
    __tablename__ = 'users_throttling_messages'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'users_throttling_messages_id_seq\')'))
    # Telegram user id.
    user_id = Column(BigInteger, nullable=False)
    # Any key from data/config/middlewares/config.
    throttling_key = Column(VARCHAR(32), nullable=False)
    # Throttling sleep time.
    sleep_time = Column(Integer, nullable=False)

    query: sql.select
