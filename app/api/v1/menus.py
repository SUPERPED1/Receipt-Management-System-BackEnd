from fastapi import APIRouter, HTTPException, status
import app.schemas as schema
from app.error import *
from app.core.static_values import *
import app.databases.menus as db
from aiomysql import IntegrityError

router = APIRouter(prefix="/v1/menus",
                   tags=["Menus"])

@router.get("/default", status_code=status.HTTP_200_OK, response_model=schema.Response[schema.menus.DefaultMenusRespone])
def get_default_menus(month:int, year:int):
    try:
        default_menus = db.get_default_menu()
        
        variables = {
            "MONTH": THAI_MONTH[month-1],
            "YEAR": year % 100
        }

        for default_menu in default_menus:
            default_menu['menu_text'] = default_menu['menu_text'].format_map(variables)

        return schema.Response(
            data = schema.menus.DefaultMenusRespone(
                default_menus=default_menus
            )
        )
    except Exception as e:
        raise e

@router.put("/default", status_code=status.HTTP_200_OK, response_model=schema.UpdateResponse[schema.menus.DefaultMenusRespone])
def update_default_menu(payload:schema.menus.UpdateDefaultMenu):
    try:
        update_list = [item.model_dump() for item in payload.default_menus]
        default_menus = db.update_default_menu(update_list)

        return schema.UpdateResponse(
            data = schema.menus.DefaultMenusRespone(
                default_menus=default_menus
            )
        )
    except Exception as e:
        raise e

# /////////////////////////////////////////////////////////////////////////

@router.get("", status_code=status.HTTP_200_OK, response_model=schema.Response[schema.menus.MenusRespone])
def get_menus(month:int, year:int):
    try:
        menus = db.get_menus()
        default_menus = db.get_default_menu()

        variables = {
            "MONTH": THAI_MONTH[month-1],
            "YEAR": year % 100
        }

        for menu in menus:
            menu['menu_text'] = menu['menu_text'].format_map(variables)
        for default_menu in default_menus:
            default_menu['menu_text'] = default_menu['menu_text'].format_map(variables)
        
        return schema.Response(
            data = schema.menus.MenusRespone(
                    menus=menus,
                    default_menus=default_menus
                )
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/{menu_id}", status_code=status.HTTP_200_OK, response_model=schema.Response[schema.menus.Menu])
def get_menu(menu_id:int):
    try:
        menu = db.get_menu(menu_id)

        return schema.Response(
            data = menu
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schema.CreateResponse[schema.menus.Menu])
def create_menu(payload:schema.menus.CreateMenu):
    try:
            
        menu = db.insert_menu(payload.menu_text)

        return schema.CreateResponse(
           data = menu
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.patch("/{menu_id}", status_code=status.HTTP_200_OK, response_model=schema.UpdateResponse[schema.menus.Menu])
def create_menu(menu_id:int, payload:schema.menus.UpdateMenu):
    try:
        menu = db.get_menu(menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu {menu_id} not found"
            )
        menu = db.update_menu(menu_id, payload.menu_text)

        return schema.CreateResponse(
           data = menu
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/{menu_id}", status_code=status.HTTP_200_OK, response_model=schema.DeleteResponse)
async def delete_menu(menu_id:int):
    try:
        menu = db.get_menu(menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu {menu_id} not found"
            )
        db.delete_menu(menu_id)
        
        return schema.DeleteResponse(data = None)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)