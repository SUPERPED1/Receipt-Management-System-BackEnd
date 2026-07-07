from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from app.core.static import *
from typing import Optional

# /////////////////////// companies /////////////////////
class Bank(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    bank_id: int
    bank_name: str
    owner_name: str

class BankResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str
    bank_list : list[Bank]

class CreateBank(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    bank_name:str
    bank_branch: Optional[str] = None
    bank_account_id: str
    owner_name: str
    owner_surname:str
    color_display:str

class CreateBankReaponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str
    insert_data: Bank

class DeleteBankResponse(BaseModel):
    message:str