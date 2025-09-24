def orders_response(
    config,
    client,
    query: dict | None = None,
    location_ids: str | list[str] | None = None,
    limit: int = 100,
    **kwargs,
):
    config = kwargs.get("config")
    cursor = None

    query = config.pop("query")
    location_ids = config.pop("location_id")
    cursor = config.pop("cursor", None)

    response = client.orders.search(
        location_ids=location_ids,
        query=query,
        cursor=cursor,
    )
    cursor = response.cursor
    orders = [order.model_dump() for order in response.orders]

    return orders
