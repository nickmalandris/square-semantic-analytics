from config.db import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import BIGINT, INTEGER, VARCHAR


class Modifiers(SQLModel, table=True):
    uid: str | None = Field(default=None, primary_key=True)
    # TODO: Add FK Reference
    object_name: str = Field(default="modifiers")
    line_item_uid: str | None = Field(default=None, foreign_key="lineitems.uid")
    catalog_object_id: str | None = Field(default=None, sa_column=Column(VARCHAR))
    catalog_version: int | None = Field(default=None, sa_column=Column(BIGINT))
    name: str | None = Field(default=None, sa_column=Column(VARCHAR))
    quantity: str | None = Field(default=None, sa_column=Column(VARCHAR))
    base_price_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    base_price_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    total_price_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    total_price_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
