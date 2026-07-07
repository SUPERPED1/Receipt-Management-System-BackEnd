from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
import json
from pydantic.alias_generators import to_camel
from app.core.static import *
from typing import Optional

class BillItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menu_text: str
    price: float

class Bill(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    id:str
    created_on: date
    bill_id: str
    customer_name: Optional[str] = None
    for_company: Optional[str] = None
    bank_name: Optional[str] = None
    bank_owner_name: Optional[str] = None
    total_price: float
    bill_status: str
    bill_detail: list[BillItem]

    @field_validator("bill_detail", mode="before")
    @classmethod
    def parse_bill_detail(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v or []

class BillResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str
    total:int
    num_page:int
    bill_list:list[Bill]

class BillNumberRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str
    receipt_id:str

class CreateBill(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    receipt_id:str
    customer_company_id:str
    for_company:int
    bank_id:int
    monthly:int
    yearly:int
    details:list[BillItem]
    
    
class BillSummary(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    total: int = 0
    number_bills: int = 0
    paid: int = 0
    unpaid: int = 0
    number_paid: int = 0
    number_unpaid: int = 0
    
    @field_validator("*", mode="before")
    @classmethod
    def none_to_zero(cls, v):
        return 0 if v is None else v