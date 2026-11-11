import app.schemas.banks as banks
import app.schemas.menus as menus
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Generic, TypeVar

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    data : T
    
class ListResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    data : list[T]
    
class CreateResponse(BaseModel, Generic[T]):
    data: T
    
class UpdateResponse(BaseModel, Generic[T]):
    data: T
    
class DeleteResponse(BaseModel):
    data:None