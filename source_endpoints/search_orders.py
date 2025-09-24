# from sqlmodel import Session
from loguru import logger
from config.db import get_session
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, IntegrityError

import pendulum
from datetime import datetime
from models.modifiers import Modifiers
from models.applied_taxes import AppliedTaxes
from models.taxes import Taxes
from models.orders import Orders
from models.tenders import Tenders
from models.applied_discounts import AppliedDiscounts
from models.line_items import LineItems
from models.discounts import Discounts
from typing import Any


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


async def incremental_config(query, session):
    """
    Function that returns the most recent start_at datetime for the query params.
    """

    try:
        start_at = await session.execute(text("SELECT MAX(CREATED_AT) FROM ORDERS"))

        query["filter"]["date_time_filter"]["created_at"]["start_at"] = (
            pendulum.instance(start_at.scalar()).to_rfc3339_string()
        )
    except ProgrammingError as e:
        print(f"Error: {e}, defaulting to full load.")
    return query


async def get_orders(
    client,
    # async_session,
    location_id: str | list[str] | None = None,
    query: dict | None = None,
    limit: int = 100,
    **kwargs,
):
    # Orders -> LineItems -> Modifiers, AppliedTaxes, AppliedDiscounts
    # Orders -> Taxes
    # Orders -> Discounts
    # Orders -> Tenders

    # async with get_session() as session:
    #     query = await incremental_config(
    #         query=query,
    #         session=session
    #     )

    response = client.orders.search(
        location_ids=location_id,
        query=query,
        limit=limit,
    )

    # cursor = response.cursor

    for result in response.orders:
        order_data = result.model_dump()
        # await write_data(object=order_data, session=get_session())
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

        line_items_data = order_data.get("line_items", None)
        if line_items_data:
            for line_item_data in line_items_data:
                line_item = LineItems(
                    uid=line_item_data.get("uid", None),
                    order_id=order.id,
                    catalog_object_id=line_item_data.get("catalog_object_id", None),
                    catalog_version=line_item_data.get("catalog_version", None),
                    name=line_item_data.get("name", None),
                    quantity=line_item_data.get("quantity", None),
                    variation_name=line_item_data.get("variation_name", None),
                    base_price_money_amount=line_item_data.get(
                        "base_price_money", None
                    ).get("amount", None),
                    base_price_money_currency=line_item_data.get(
                        "base_price_money", None
                    ).get("currency", None),
                    gross_sales_money_amount=line_item_data.get(
                        "gross_sales_money", None
                    ).get("amount", None),
                    gross_sales_money_currency=line_item_data.get(
                        "gross_sales_money", None
                    ).get("currency", None),
                    total_tax_money_amount=line_item_data.get(
                        "total_tax_money", None
                    ).get("amount", None),
                    total_tax_money_currency=line_item_data.get(
                        "total_tax_money", None
                    ).get("currency", None),
                    total_discount_money_amount=line_item_data.get(
                        "total_discount_money", None
                    ).get("amount", None),
                    total_discount_money_currency=line_item_data.get(
                        "total_discount_money", None
                    ).get("currency", None),
                    total_money_amount=line_item_data.get("total_money", None).get(
                        "amount", None
                    ),
                    total_money_currency=line_item_data.get("total_money", None).get(
                        "currency", None
                    ),
                    variation_total_price_money_amount=line_item_data.get(
                        "variation_total_price_money", None
                    ).get("amount", None),
                    variation_total_price_money_currency=line_item_data.get(
                        "variation_total_price_money", None
                    ).get("currency", None),
                    total_service_charge_money_amount=line_item_data.get(
                        "total_service_charge_money", None
                    ).get("amount", None),
                    total_service_charge_money_currency=line_item_data.get(
                        "total_service_charge_money", None
                    ).get("currency", None),
                    item_type=line_item_data.get("item_type", None),
                )
                async with get_session() as session:
                    await write_data(object=line_item, session=session)

                modifiers_data = line_item_data.get("modifiers", None)
                if modifiers_data:
                    for modifier_data in modifiers_data:
                        modifier = Modifiers(
                            uid=modifier_data.get("uid", None),
                            catalog_object_id=modifier_data.get(
                                "catalog_object_id", None
                            ),
                            catalog_version=modifier_data.get("catalog_version", None),
                            name=modifier_data.get("name", None),
                            quantity=modifier_data.get("quantity", None),
                            base_price_money_amount=modifier_data.get(
                                "base_price_money", None
                            ).get("amount", None),
                            base_price_money_currency=modifier_data.get(
                                "base_price_money", None
                            ).get("currency", None),
                            total_price_money_amount=modifier_data.get(
                                "total_price_money", None
                            ).get("amount", None),
                            total_price_money_currency=modifier_data.get(
                                "total_price_money", None
                            ).get("currency", None),
                        )
                        async with get_session() as session:
                            await write_data(object=modifier, session=session)

                applied_taxes_data = line_item_data.get("applied_taxes", None)
                if applied_taxes_data:
                    for applied_tax_data in applied_taxes_data:
                        applied_tax = AppliedTaxes(
                            uid=applied_tax_data.get("uid", None),
                            line_item_uid=line_item_data.get("uid", None),
                            tax_uid=applied_tax_data.get("tax_uid", None),
                            applied_money_amount=applied_tax_data.get(
                                "applied_money", None
                            ).get("amount", None),
                            applied_money_currency=applied_tax_data.get(
                                "applied_money", None
                            ).get("currency", None),
                            auto_applied=applied_tax_data.get("auto_applied", None),
                        )

                        async with get_session() as session:
                            await write_data(object=applied_tax, session=session)

                applied_discounts_data = line_item_data.get("applied_discounts", None)
                if applied_discounts_data:
                    for applied_discount_data in applied_discounts_data:
                        applied_discount = AppliedDiscounts(
                            uid=applied_discount_data.get("uid", None),
                            line_item_uid=line_item_data.get("uid", None),
                            discount_uid=applied_discount_data.get(
                                "discount_uid", None
                            ),
                            applied_money_amount=applied_discount_data.get(
                                "applied_money", None
                            ).get("amount", None),
                            applied_money_currency=applied_discount_data.get(
                                "applied_money", None
                            ).get("currency", None),
                        )
                        async with get_session() as session:
                            await write_data(object=applied_discount, session=session)

        taxes_data = order_data.get("taxes", None)
        if taxes_data:
            for tax_data in taxes_data:
                tax = Taxes(
                    uid=tax_data.get("uid", None),
                    order_id=order.id,
                    catalog_object_id=tax_data.get("catalog_object_id", None),
                    catalog_version=tax_data.get("catalog_version", None),
                    name=tax_data.get("name", None),
                    percentage=tax_data.get("percentage", None),
                    type=tax_data.get("type", None),
                    scope=tax_data.get("scope", None),
                    applied_money_amount=tax_data.get("applied_money", None).get(
                        "amount", None
                    ),
                    applied_money_currency=tax_data.get("applied_money", None).get(
                        "currency", None
                    ),
                )
                async with get_session() as session:
                    await write_data(object=tax, session=session)

        discounts = order_data.get("discounts", None)
        if discounts:
            for discount_data in discounts:
                discount = Discounts(
                    uid=discount_data.get("uid", None),
                    order_id=order.id,
                    catalog_object_id=discount_data.get("catalog_object_id", None),
                    catalog_version=discount_data.get("catalog_version", None),
                    name=discount_data.get("name", None),
                    percentage=discount_data.get("percentage", None),
                    applied_money_amount=discount_data.get("applied_money", None).get(
                        "amount", None
                    ),
                    applied_money_currency=discount_data.get("applied_money", None).get(
                        "currency", None
                    ),
                    type=discount_data.get("type", None),
                    scope=discount_data.get("scope", None),
                )
                async with get_session() as session:
                    await write_data(object=discount, session=session)

        tenders_data = order_data.get("tenders", None)
        print(f"TENDERS DATA####### \n {tenders_data}")
        if tenders_data:
            for tender_data in tenders_data:
                # break
                tender = Tenders(
                    id=tender_data.get("id", None),
                    order_id=order.id,
                    location_id=tender_data.get("location_id", None),
                    transaction_id=tender_data.get("transaction_id", None),
                    created_at=datetime.fromisoformat(
                        pendulum.parse(
                            tender_data.get("created_at", None)
                        ).to_datetime_string()
                    ),
                    amount_money_amount=tender_data.get("amount_money", None).get(
                        "amount", None
                    ),
                    amount_money_currency=tender_data.get("amount_money", None).get(
                        "currency", None
                    ),
                    processing_fee_money_amount=tender_data.get(
                        "processing_fee_money", None
                    ).get("amount"),
                    processing_fee_money_currency=tender_data.get(
                        "processing_fee_money", None
                    ).get("currency"),
                    customer_id=tender_data.get("customer_id", None),
                    type=tender_data.get("type", None),
                    card_details_status=tender_data.get("card_details", None).get(
                        "status", None
                    )
                    if tender_data.get("card_details") is not None
                    else None,
                    card_details_card_brand=tender_data.get("card_details", None)
                    .get("card", None)
                    .get("card_brand", None)
                    if tender_data.get("card_details") is not None
                    else None,
                    card_details_last_4=tender_data.get("card_details", None)
                    .get("card", None)
                    .get("last_4", None)
                    if tender_data.get("card_details") is not None
                    else None,
                    card_details_fingerprint=tender_data.get("card_details", None)
                    .get("card", None)
                    .get("fingerprint", None)
                    if tender_data.get("card_details") is not None
                    else None,
                    card_details_entry_method=tender_data.get("card_details", None).get(
                        "entry_method", None
                    )
                    if tender_data.get("card_details") is not None
                    else None,
                    cash_details_buyer_tendered_money=tender_data.get(
                        "cash_details", None
                    )
                    .get("buyer_tendered_money", None)
                    .get("amount")
                    if tender_data.get("cash_details") is not None
                    else None,
                    cash_details_buyer_tendered_currency=tender_data.get(
                        "cash_details", None
                    )
                    .get("buyer_tendered_money", None)
                    .get("currency")
                    if tender_data.get("cash_details") is not None
                    else None,
                    entry_method=tender_data.get("entry_method", None),
                )
                async with get_session() as session:
                    await write_data(object=tender, session=session)
