from config.db import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import INTEGER, BIGINT, VARCHAR


class Taxes(SQLModel, table=True):
    uid: str | None = Field(default=None, primary_key=True)
    object_name: str = Field(default="taxes")
    order_id: str | None = Field(default=None, foreign_key="orders.id")
    catalog_object_id: str | None = Field(default=None, sa_column=Column(VARCHAR))
    catalog_version: int | None = Field(default=None, sa_column=Column(BIGINT))
    name: str | None = Field(default=None, sa_column=Column(VARCHAR))
    percentage: str | None = Field(default=None, sa_column=Column(VARCHAR))
    type: str | None = Field(default=None, sa_column=Column(VARCHAR))
    scope: str | None = Field(default=None, sa_column=Column(VARCHAR))
    applied_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    applied_money_currency: str | None = Field(default=None, sa_column=Column(VARCHAR))
