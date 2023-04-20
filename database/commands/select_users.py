from typing import List, Tuple

from asyncpg import UniqueViolationError

from database import UsersMessages

from sqlalchemy import select, func


async def select_users() -> List[Tuple[int]]:
    '''
    :return: Tuples with telegram users id in list.
    '''

    return await select([func.distinct(UsersMessages.user_id)]).gino.all()
