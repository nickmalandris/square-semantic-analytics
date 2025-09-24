from config.db import init_db, get_session
from authenticate import get_square_client
from pathlib import Path
from loguru import logger
from benedict import benedict
import asyncio
from utils.cursor_manager import get_cursor

# from source_endpoints.search_orders import get_orders


client = get_square_client()

api_config_path = Path(__file__).parent / "source_endpoints"

config_dict = {}
for config_path in api_config_path.glob("config/*"):
    config = benedict.from_yaml(config_path)
    config_dict[config.get("object_name")] = config


"""
    {
        orders: {config},
        payments: {config}
    }
    --> get cursors (if none keep config query as default)
    --> if cursor results update config query
    Challenge --> returning more cursor objects for a given endpoint.
"""

# get_payments(
#     client=client,
#     session=Session(engine),
#     sort_field=config.pop("sort_field"),
#     sort_order=config.pop("sort_order"),
#     begin_time=config.pop("begin_time"),
#     limit=config.pop("limit"),
#     **config,
# )


async def main():
    deps_conf = config_dict.copy()
    for k, v in config_dict.items():
        dependencies = config_dict[k].get("dependencies", None)
        if dependencies:
            for dependency in dependencies:
                deps_conf[dependency] = v

    await init_db()

    cursor_list = True

    while cursor_list:
        async with get_session() as session:
            cursor_list = await get_cursor(session=session)
            logger.info(f"CURSOR: {cursor_list}")

            if cursor_list:
                for obj in cursor_list:
                    deps_conf[obj.object_name].update({"cursor": obj.cursor_id})
                    deps_conf[obj.object_name]["query"].pop("filter")

            config_list = [{k: v} for k, v in deps_conf.items()]

            logger.info(f"Config List: \n{config_list}")

            # orders = orders_response(config=deps_conf)

            # orders_obj = await base_orders(orders=orders)

            # await write_cursor(
            #     object_name=extra_orders.get("object_name", "orders"),
            #     cursor=cursor,
            #     session=session,
            # )

    # # Clean uo pooled connections

    # await engine.dispose()


asyncio.run(main())
