from config.db import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import BIGINT, INTEGER, VARCHAR


class LineItems(SQLModel, table=True):
    uid: str | None = Field(default=None, primary_key=True)
    order_id: str | None = Field(
        default=None, foreign_key="orders.id"
    )  # , foreign_key="order.id")
    object_name: str = Field(default="lineitems")
    catalog_object_id: str | None = Field(default=None, sa_column=Column(VARCHAR))
    catalog_version: int | None = Field(default=None, sa_column=Column(BIGINT))
    name: str | None = Field(default=None, sa_column=Column(VARCHAR))
    quantity: str | None = Field(default=None, sa_column=Column(VARCHAR))
    variation_name: str | None = Field(default=None, sa_column=Column(VARCHAR))
    base_price_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    base_price_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    gross_sales_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    gross_sales_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    total_tax_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    total_tax_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    total_discount_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    total_discount_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    total_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    total_money_currency: str | None = Field(default=None, sa_column=Column(VARCHAR))
    variation_total_price_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    variation_total_price_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    total_service_charge_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    total_service_charge_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    item_type: str | None = Field(default=None, sa_column=Column(VARCHAR))
