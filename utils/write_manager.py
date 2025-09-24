from loguru import logger
from config.db import select
from models.cursor import Cursor
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import Any
import pendulum
from datetime import datetime


async def write_data(object: Any, session):
    """Function to insert objects to tables"""
    try:
        session.add(object)
        await session.commit()
    except IntegrityError as e:
        if e.orig.pgcode == "23505":
            logger.info(f"Unique constraint violation: {e}")
            await session.rollback()  # Keep this - you want to rollback immediately
            # Don't re-raise since you're handling this gracefully
        else:
            logger.info(f"Uncaught Error: {e}")
            logger.info(f"Error Origin: {e.orig}")
            logger.info(f"Error Origin PG Code: {e.orig.pgcode}")
            raise  # Let the context manager handle other IntegrityErrors
    except Exception as e:
        logger.debug(f"New Un-handled Error: {e}")
        raise


async def write_cursor(object_name: str, cursor: str, session):
    try:
        statement = select(Cursor).where(Cursor.object_name == object_name)
        results = await session.execute(statement)
        cursor_res = results.one()
        logger.info(f"Attemptmting to update {object_name} cursor.")
        logger.info(f"Updating cursor record to: {cursor} for obejct {object_name}")

        try:
            cursor_res.cursor_id = cursor

            await session.add(cursor_res)
            await session.commit()
            await session.close()

        except AttributeError as e:
            logger.info(f"Error: {e}")
            logger.info(f"Current Cursor ID: {cursor_res}")
            logger.info(f"New Cursor ID: {cursor}")

    except NoResultFound as e:
        logger.info(
            f"No Cursor Result for {object_name}. {e}\n Inserting cursor record: {cursor} for obejct {object_name}"
        )
        obj = Cursor(
            cursor_id=cursor,
            object_name=object_name,
            # TODO Update to max(created_at) time
            last_updated_at=datetime.fromisoformat(
                (pendulum.now("UTC").to_datetime_string())
            ),
        )
        await session.add(obj)
        await session.commit()
        await session.close()
