from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from app.core.static_values import *

# /////////////////////// menus //////////////////
class Menu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menu_id: int
    menu_text: str
    
class DefaultMenu(Menu):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menu_order : int

class MenusRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menus : list[Menu]
    default_menus : list[DefaultMenu]

class DefaultMenusRespone(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    default_menus : list[DefaultMenu]

class CreateMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menu_text: str
    
class UpdateMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menu_text: str

# class CreateMenuRespone(BaseModel):
#     model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
#     message:str = "Insert menu successfully"
#     insert_data: Menu

class UpdateDefaultItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    menu_id:int
    menu_order:int

class UpdateDefaultMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
    default_menus: list[UpdateDefaultItem]

# class DeleteMenuRespone(BaseModel):
#     model_config = ConfigDict(alias_generator=to_camel , populate_by_name=True)
#     message:str = "Delete menu successfully"