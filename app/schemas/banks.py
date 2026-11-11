from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from app.core.static_values import *
from typing import Optional, Generic

# /////////////////////// companies /////////////////////
class BankBase(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    bank_name: str
    branch: str | None = None
    bank_account: str
    owner_name: str
    owner_surname: str
    limit_used: int
    color: str


class CreateBank(BankBase):
    pass

class UpdateBank(BankBase):
    pass

class Bank(BankBase):
    bank_id: int
    model_config = ConfigDict(
            alias_generator=to_camel,
            populate_by_name=True
        )