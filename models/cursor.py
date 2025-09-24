from config.db import SQLModel, Field
from datetime import datetime
from sqlalchemy.dialects.postgresql import VARCHAR, TIMESTAMP


class Cursor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cursor_id: str | None = Field(default=None, sa_column=VARCHAR)
    object_name: str | None = Field(default=None, sa_column=VARCHAR)
    last_updated_at: datetime | None = Field(default=None, sa_column=TIMESTAMP)
