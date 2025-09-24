# from pydanitc import BaseModel, Field
from typing import Optional, ClassVar
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import (
    model_validator,
    BaseModel,
)


class Payments(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)

    object_name: str = Field(default="payments")
    # amount_money: str | None = Field(default=None)
    amount_money_amount: int = Field(default=None)
    amount_money_currency: str = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    status: str | None = Field(default=None)
    source_type: str | None = Field(default=None)

    # card_details: str | None = Field(default=None)

    # entry_method: str | None = Field(default=None)
    # cvv_status: str | None = Field(default=None)
    # avs_status: str | None = Field(default=None)
    # auth_result_code: str | None = Field(default=None)
    # application_identifier: str | None = Field(default=None)
    # application_name: str | None = Field(default=None)
    # application_cryptogram: str | None = Field(default=None)
    # verification_method: str | None = Field(default=None)
    # verification_results: str | None = Field(default=None)
    # statement_description: str | None = Field(default=None)

    # card_payment_timeline: str | None = Field(default=None)
    # card_payment_timeline_authorized_at: datetime | None = Field(default=None)
    # card_payment_timeline_captured_at: datetime | None = Field(default=None)
    customer_id: str | None = Field(default=None)

    # total_money: str | None = Field(default=None)
    # approved_money: str | None = Field(default=None)

    total_money_amount: int | None = Field(default=None)
    total_money_currency: str | None = Field(default=None)
    approved_money_amount: int | None = Field(default=None)
    approved_money_currency: str | None = Field(default=None)
    delay_action: str | None = Field(default=None)
    delayed_until: datetime | None = Field(default=None)

    # device_details: str | None = Field(default=None)

    device_details_device_id: str | None = Field(default=None)
    device_details_device_name: str | None = Field(default=None)
    device_details_device_installation_id: str | None = Field(default=None)
    # processing_fee: List[dict] | None = Field(default=None)

    team_member_id: str | None = Field(default=None)

    application_details_sqaure_product: str | None = Field(default=None)

    # application_details: str | None = Field(default=None)

    order_id: str | None = Field(default=None)
    location_id: str | None = Field(default=None)
    receipt_url: str | None = Field(default=None)
    version_token: str | None = Field(default=None)


class BasePaymentModel(BaseModel):
    id: str | None = Field(default=None, primary_key=True)

    amount_money: dict | None = Field(default=None)
    amount_money_amount: Optional[int | None] = Field(default=None)
    amount_money_currency: str = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    status: str | None = Field(default=None)
    source_type: str | None = Field(default=None)

    # card_details: dict | None = Field(default=None)

    # entry_method: str | None = Field(default=None)
    # cvv_status: str | None = Field(default=None)
    # avs_status: str | None = Field(default=None)
    # auth_result_code: str | None = Field(default=None)
    # application_identifier: str | None = Field(default=None)
    # application_name: str | None = Field(default=None)
    # application_cryptogram: str | None = Field(default=None)
    # verification_method: str | None = Field(default=None)
    # verification_results: str | None = Field(default=None)
    # statement_description: str | None = Field(default=None)

    # card_payment_timeline: dict | None = Field(default=None)
    # card_payment_timeline_authorized_at: datetime | None = Field(default=None)
    # card_payment_timeline_captured_at: str | None = Field(default=None)
    customer_id: str | None = Field(default=None)

    total_money: dict | None = Field(default=None)
    approved_money: dict | None = Field(default=None)

    total_money_amount: int | None = Field(default=None)
    total_money_currency: str | None = Field(default=None)
    approved_money_amount: int | None = Field(default=None)
    approved_money_currency: str | None = Field(default=None)
    delay_action: str | None = Field(default=None)
    delayed_until: datetime | None = Field(default=None)

    device_details: dict | None = Field(default=None)

    device_details_device_id: str | None = Field(default=None)
    device_details_device_name: str | None = Field(default=None)
    device_details_device_installation_id: str | None = Field(default=None)
    # processing_fee: List[dict] | None = Field(default=None)

    team_member_id: str | None = Field(default=None)

    application_details: dict | None = Field(default=None)
    application_details_sqaure_product: str | None = Field(default=None)

    order_id: str | None = Field(default=None)
    location_id: str | None = Field(default=None)
    receipt_url: str | None = Field(default=None)
    version_token: str | None = Field(default=None)

    _flatten_mapping: ClassVar[dict] = {
        "amount_money": {
            "amount": "amount_money_amount",
            "currency": "amount_money_currency",
        },
        "total_money": {
            "amount": "total_money_amount",
            "currency": "total_money_currency",
        },
        "approved_money": {
            "amount": "approved_money_amount",
            "currency": "approved_money_currency",
        },
        "device_details": {
            "device_id": "device_details_device_id",
            "device_name": "device_details_device_name",
            "device_installation_id": "device_details_device_installation_id",
        },
        # "card_details": {
        #     "status": "card_details_status",
        #     "card": {
        #         "card_brand": "card_details_card_brand",
        #         "last_4": "card_details_last_4",
        #     },
        # },
        # "card_payment_timeline": {
        #     "authorized_at": "card_payment_timeline_authorized_at",
        #     "captured_at": "card_payment_timeline_captured_at",
        # },
        "application_details": {"square_product": "application_details_square_product"},
    }

    @model_validator(mode="before")
    @classmethod
    def flatten_dict_fields(cls, data):
        if not isinstance(data, dict):
            return data
        for dict_field, field_mapping in cls._flatten_mapping.items():
            dict_value = data.get(dict_field)
            if dict_value and isinstance(dict_value, dict):
                for source_key, target_field in field_mapping.items():
                    # Only set if target field isn't already provided
                    data.setdefault(target_field, dict_value.get(source_key))

        return data
