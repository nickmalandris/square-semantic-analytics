from config.db import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR


class AppliedDiscounts(SQLModel, table=True):
    uid: str | None = Field(default=None, primary_key=True)
    object_name: str = Field(default="applieddiscounts")
    # TODO: Add FK Reference
    line_item_uid: str | None = Field(default=None, foreign_key="lineitems.uid")
    discount_uid: str | None = Field(default=None, sa_column=Column(VARCHAR))
    applied_money_amount: int | None = Field(default=None, sa_column=Column(INTEGER))
    applied_money_currency: str | None = Field(default=None, sa_column=Column(VARCHAR))
