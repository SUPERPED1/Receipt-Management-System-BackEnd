from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from app.core.static import *

# /////////////////////// customers //////////////////
class Customer(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    company_id: str
    company_name: str

class CustomerRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str
    customer_list : list[Customer]