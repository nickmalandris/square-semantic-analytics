from config.db import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, VARCHAR


class AppliedTaxes(SQLModel, table=True):
    uid: str | None = Field(default=None, primary_key=True)
    object_name: str = Field(default="appliedtaxes")
    # TODO: Add FK Reference
    line_item_uid: str | None = Field(default=None, foreign_key="lineitems.uid")
    tax_uid: str | None = Field(default=None, sa_column=Column(VARCHAR))
    applied_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    applied_money_currency: int | None = Field(default=None, sa_column=Column(VARCHAR))
    auto_applied: bool | None = Field(default=None, sa_column=Column(BOOLEAN))
