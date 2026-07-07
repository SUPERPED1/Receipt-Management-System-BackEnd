from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from app.core.static import *

# /////////////////////// menus //////////////////
class Menu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menu_id: int
    menu_text: str

# class MenuDetail(BaseModel):
#     addon_type:int
#     is_default:bool
#     display_order:int

class MenusRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message : str
    menu_list : list[Menu]
    default_menus : list[Menu]

class DefaultMenusResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message : str
    default_menus : list[Menu]

class MenuRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message : str
    menu_list : list[Menu]

class CreateMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menu_text: str
    has_month:bool = False
    has_year:bool = False

class CreateMenuRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str = "Insert menu successfully"
    insert_data: Menu

class UpdateDefaultItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    order:int
    id:int
    name:str

class UpdateDefaultMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    default_list: list[UpdateDefaultItem]

class DeleteMenuRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    message:str = "Delete menu successfully"