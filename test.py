from pydantic import BaseModel, Field
from typing import Optional


class UserData(BaseModel):
    first_name: str = Field(alias="first")
    last_name: str = Field(alias="last")
    email: Optional[str] = None


json_data = {"name": {"first": "John", "last": "Doe"}, "email": "john.doe@example.com"}

user = UserData.model_validate(json_data)
print(user)
