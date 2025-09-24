"""
Manager the cursor value for a given table.


flow of code execution should be:
-> check cursor table for cursor value (if any)
if I have the cursor for each table object.
Need to call each API concurrently
might need a mapping table to a callable object.
{
    object_name: callable(),
    object_name: callable(),
    object_name: callable(),
}
-> update the query
-> call api
-> return result
-> write the cursor as a checkpoint - Will need cursor, current datetime and then also the object name.

"""

from config.db import AsyncSession, select
from models.cursor import Cursor
from sqlalchemy.exc import ProgrammingError, NoResultFound
from loguru import logger


async def get_cursor(session: AsyncSession) -> list[Cursor]:
    """
    args
        - session: AsyncSession - database session
    Function to get the cursor for each of the objects.
    """
    cursor = None
    try:
        statement = select(Cursor)
        results = await session.execute(statement)
        cursor = results.scalars().all()
    except ProgrammingError as e:
        logger.info(f"Error defaulting to None: \n{e}")
    except NoResultFound as e:
        logger.info(f"No result found: \n{e}")

    return cursor
