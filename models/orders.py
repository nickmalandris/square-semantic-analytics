from datetime import datetime
from config.db import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import TIMESTAMP, INTEGER, VARCHAR

from pydantic import BaseModel


class Orders(SQLModel, table=True):
    id: str = Field(primary_key=True)
    # object_name: str = Field(default='orders', exclude=True)
    location_id: str | None = Field(default=None, sa_column=Column(VARCHAR))
    created_at: datetime | None = Field(default=None, sa_column=Column(TIMESTAMP))
    updated_at: datetime | None = Field(default=None, sa_column=Column(TIMESTAMP))
    state: str | None = Field(default=None, sa_column=Column(VARCHAR))
    # total_tax_money: dict = Field(exclude=True)
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
    total_tip_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    total_tip_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    total_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    total_money_currency: str | None = Field(default=None, sa_column=Column(VARCHAR))
    closed_at: datetime | None = Field(default=None, sa_column=Column(TIMESTAMP))
    total_service_charge_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    total_service_charge_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    return_amounts_total_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    return_amounts_total_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    return_amounts_tax_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    return_amounts_tax_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    return_amounts_discount_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    return_amounts_discount_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    return_amounts_tip_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    return_amounts_tip_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    return_amounts_service_charge_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    return_amounts_service_charge_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    net_amounts_total_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    net_amounts_total_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    net_amounts_tax_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    net_amounts_tax_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    net_amounts_discount_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    net_amounts_discount_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    net_amounts_tip_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    net_amounts_tip_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    net_amounts_service_charge_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    net_amounts_service_charge_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )
    ticket_name: str | None = Field(default=None, sa_column=Column(VARCHAR))
    net_amount_due_money_amount: int | None = Field(
        default=None, sa_column=Column(INTEGER)
    )
    net_amount_due_money_currency: str | None = Field(
        default=None, sa_column=Column(VARCHAR)
    )


class BaseOrderModel(BaseModel):
    id: str | None = Field(default=None)
    location_id: str | None = Field(default=None)
    line_items: list[dict | list] | None = Field(default=None)
    taxes: list[dict] | None = Field(default=None)
    discounts: list[dict] | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    state: str | None = Field(default=None)
    total_tax_money: dict | None = Field(default=None)
    total_discount_money: dict | None = Field(default=None)
    total_tip_money: dict | None = Field(default=None)
    total_money: dict | None = Field(default=None)
    closed_at: datetime | None = Field(default=None)
    tenders: list[dict] | None = Field(default=None)
    total_service_charge_money: dict | None = Field(default=None)
    return_amounts: dict | None = Field(default=None)
    tax_money: dict | None = Field(default=None)
    discount_money: dict | None = Field(default=None)
    tip_money: dict | None = Field(default=None)
    service_charge_money: dict | None = Field(default=None)
    net_amounts: dict | None = Field(default=None)
    tax_money: dict | None = Field(default=None)
    discount_money: dict | None = Field(default=None)
    tip_money: dict | None = Field(default=None)
    service_charge_money: dict | None = Field(default=None)
    source: dict | None = Field(default=None)
    ticket_name: str | None = Field(default=None)
    net_amount_due_money: dict | None = Field(default=None)

    # _flatten_mapping: ClassVar[dict] = {
    # }

    # @model_validator(mode="before")
    # @classmethod
    # def flatten_dict_fields(cls, data):
    #     if not isinstance(data, dict):
    #         return data
    #     for dict_field, field_mapping in cls._flatten_mapping.items():
    #         dict_value = data.get(dict_field)
    #         if dict_value and isinstance(dict_value, dict):
    #             for source_key, target_field in field_mapping.items():
    #                 # Only set if target field isn't already provided
    #                 data.setdefault(target_field, dict_value.get(source_key))

    #     return data
