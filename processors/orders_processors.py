from models.orders import Orders
from datetime import datetime
import pendulum
from config.db import get_session
from utils.write_manager import write_data


async def base_orders(
    orders: list[dict],
):
    for order_data in orders:
        order = Orders(
            id=order_data.get("id", None),
            location_id=order_data.get("location_id", None),
            created_at=datetime.fromisoformat(
                pendulum.parse(order_data.get("created_at", None)).to_datetime_string()
            ),
            updated_at=datetime.fromisoformat(
                pendulum.parse(order_data.get("updated_at", None)).to_datetime_string()
            ),
            state=order_data.get("state", None),
            total_tax_money_amount=order_data.get("total_tax_money", None).get(
                "amount", None
            ),
            total_tax_money_currency=order_data.get("total_tax_money", None).get(
                "currency", None
            ),
            total_discount_money_amount=order_data.get(
                "total_discount_money", None
            ).get("amount", None),
            total_discount_money_currency=order_data.get(
                "total_discount_money", None
            ).get("currency", None),
            total_tip_money_amount=order_data.get("total_tip_money", None).get(
                "amount", None
            ),
            total_tip_money_currency=order_data.get("total_tip_money", None).get(
                "currency", None
            ),
            total_money_amount=order_data.get("total_money", None).get("amount", None),
            total_money_currency=order_data.get("total_money", None).get(
                "currency", None
            ),
            closed_at=datetime.fromisoformat(
                pendulum.parse(order_data.get("closed_at", None)).to_datetime_string()
            ),
            total_service_charge_money_amount=order_data.get(
                "total_service_charge_money", None
            ).get("amount", None),
            total_service_charge_money_currency=order_data.get(
                "total_service_charge_money", None
            ).get("currency", None),
            return_amounts_total_money_amount=order_data.get("return_amounts", None)
            .get("total_money", None)
            .get("amount", None),
            return_amounts_total_money_currency=order_data.get("return_amounts", None)
            .get("total_money", None)
            .get("currency", None),
            return_amounts_tax_money_amount=order_data.get("return_amounts", None)
            .get("tax_money", None)
            .get("amount", None),
            return_amounts_tax_money_currency=order_data.get("return_amounts", None)
            .get("tax_money", None)
            .get("currency", None),
            return_amounts_discount_money_amount=order_data.get("return_amounts", None)
            .get("discount_money", None)
            .get("amount", None),
            return_amounts_discount_money_currency=order_data.get(
                "return_amounts", None
            )
            .get("discount_money", None)
            .get("currency", None),
            return_amounts_tip_money_amount=order_data.get("return_amounts", None)
            .get("tip_money", None)
            .get("amount", None),
            return_amounts_tip_money_currency=order_data.get("return_amounts", None)
            .get("tip_money", None)
            .get("currency", None),
            return_amounts_service_charge_money_amount=order_data.get(
                "return_amounts", None
            )
            .get("service_charge_money", None)
            .get("amount", None),
            return_amounts_service_charge_money_currency=order_data.get(
                "return_amounts", None
            )
            .get("service_charge_money", None)
            .get("currency", None),
            net_amounts_total_money_amount=order_data.get("return_amounts", None)
            .get("total_money", None)
            .get("amount", None),
            net_amounts_total_money_currency=order_data.get("net_amounts", None)
            .get("total_money", None)
            .get("currency", None),
            net_amounts_tax_money_amount=order_data.get("net_amounts", None)
            .get("tax_money", None)
            .get("amount", None),
            net_amounts_tax_money_currency=order_data.get("net_amounts", None)
            .get("tax_money", None)
            .get("currency", None),
            net_amounts_discount_money_amount=order_data.get("net_amounts", None)
            .get("discount_money", None)
            .get("amount", None),
            net_amounts_discount_money_currency=order_data.get("net_amounts", None)
            .get("discount_money", None)
            .get("currency", None),
            net_amounts_tip_money_amount=order_data.get("net_amounts", None)
            .get("tip_money", None)
            .get("amount", None),
            net_amounts_tip_money_currency=order_data.get("net_amounts", None)
            .get("tip_money", None)
            .get("currency", None),
            net_amounts_service_charge_money_amount=order_data.get("net_amounts", None)
            .get("service_charge_money", None)
            .get("amount", None),
            net_amounts_service_charge_money_currency=order_data.get(
                "net_amounts", None
            )
            .get("service_charge_money", None)
            .get("currency", None),
            ticket_name=order_data.get("ticket_name", None),
            net_amount_due_money_amount=order_data.get(
                "net_amount_due_money", None
            ).get("amount", None),
            net_amount_due_money_currency=order_data.get(
                "net_amount_due_money", None
            ).get("currency", None),
        )
        async with get_session() as session:
            await write_data(object=order, session=session)

    # print(response.model_dump())


# async def get_orders(
#     client,
#     # async_session,
#     location_id: str | list[str] | None = None,
#     query: dict | None = None,
#     limit: int = 100,
#     **kwargs,
# ):
#     # Orders -> LineItems -> Modifiers, AppliedTaxes, AppliedDiscounts
#     # Orders -> Taxes
#     # Orders -> Discounts
#     # Orders -> Tenders

#     # async with get_session() as session:
#     #     query = await incremental_config(
#     #         query=query,
#     #         session=session
#     #     )

#     response = client.orders.search(
#         location_ids=location_id,
#         query=query,
#         limit=limit,
#     )

#     # cursor = response.cursor

#     for result in response.orders:
#         order_data = result.model_dump()
