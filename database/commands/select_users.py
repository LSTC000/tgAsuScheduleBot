from typing import List, Tuple

from loader import db, logger

from asyncpg import UniqueViolationError

from database import UsersMessages


async def select_users() -> List[Tuple[int]]:
    '''
    :return: Tuples with telegram users id in list.
    '''

    users = await db.select([db.func.distinct(UsersMessages.user_id)]).gino.all()
    return users
