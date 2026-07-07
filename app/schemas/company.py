from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from app.core.static import *

# /////////////////////// companies /////////////////////
class Company(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    company_id: int
    company_name: str

class CompanyResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str
    company_list : list[Company]

class CreateCompany(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    company_id: str
    company_name: str
    prefix:str
    company_detail:str

class CreateCompanyRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str = "Insert company successfully"
    insert_data: Company

class DeleteCompanyRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str = "Delete company successfully"