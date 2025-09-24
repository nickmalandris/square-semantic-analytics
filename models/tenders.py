from datetime import datetime
from config.db import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIMESTAMP


class Tenders(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    object_name: str = Field(default="tenders")
    order_id: str | None = Field(default=None, foreign_key="orders.id")
    location_id: str | None = Field(default=None, sa_column=Column(VARCHAR))
    transaction_id: str | None = Field(default=None, sa_column=Column(VARCHAR))
    created_at: datetime | None = Field(default=None, sa_column=Column(TIMESTAMP))
    amount_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    amount_money_currency: str | None = Field(default=None, sa_column=Column(VARCHAR))
    processing_fee_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    processing_fee_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    customer_id: str | None = Field(default=None, sa_column=Column(VARCHAR))
    type: str | None = Field(default=None, sa_column=Column(VARCHAR))
    card_details_status: str | None = Field(default=None, sa_column=Column(VARCHAR))
    card_details_card_brand: str | None = Field(default=None, sa_column=Column(VARCHAR))
    card_details_last_4: int | None = Field(default=None, sa_column=Column(INTEGER))
    card_details_fingerprint: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    card_details_entry_method: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    cash_details_buyer_tendered_money: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    cash_details_buyer_tendered_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
