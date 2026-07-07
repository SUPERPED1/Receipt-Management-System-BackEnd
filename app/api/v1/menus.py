from fastapi import APIRouter, HTTPException, status
import app.repositories as repo
from app.schemas import MenusRespone, DefaultMenusResponse, CreateMenu, CreateMenuRespone, UpdateDefaultMenu, DeleteMenuRespone
from aiomysql import IntegrityError
from typing import Optional

router = APIRouter(prefix="/v1/menus",
                   tags=["Menus"])

thai_months = [
        "", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
        "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
    ]

@router.get("", status_code=status.HTTP_200_OK, response_model=MenusRespone)
async def get_menus(month:Optional[int]):
    try:
        menus = await repo.get_all_menus()
        for menu in menus:
            if menu["addon_type"] == 1:
                menu["menu_text"] = f"{menu['menu_text']} เดือน {thai_months[month]}"

        default_menu = await repo.get_default_menu()
        for menu in default_menu:
            if menu["addon_type"] == 1:
                menu["menu_text"] = f"{menu['menu_text']} เดือน {thai_months[month]}"

        return MenusRespone(
            message="Query_success",
            menu_list=menus,
            default_menus=default_menu,
        )
    except Exception as e:
        # logger.warning()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_menu(payload:CreateMenu):
    try:
        if payload.has_month and payload.has_year:
            addon_type = 3
        elif payload.has_year:
            addon_type = 2
        elif payload.has_month:
            addon_type = 1
        else:
            addon_type = 0
            
        new_id = await repo.insert_menu(payload.menu_text ,addon_type)

        return CreateMenuRespone(
            message="Create menu succesfully",
            insert_data={
                "menu_id":new_id,
                "menu_text":payload.menu_text,
            }
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
@router.put("")
async def update_entire_menu():
    pass

@router.put("/default", response_model=DefaultMenusResponse)
async def update_default_menu(payload:UpdateDefaultMenu):
    try:
        # Cleaning
        update_list = []
        for i, p in enumerate(payload.default_list, start=1):
            update_list.append((i, p.id))

        await repo.update_default_menu(update_list)

        default_menu = await repo.get_default_menu()

        return DefaultMenusResponse(
            message="Query_success",
            default_menus=default_menu,
        )
    except Exception as e:
        raise e

@router.patch("/{menu_id}")
async def update_specfic_feild_menu():
    pass

@router.delete("/{menu_id}", status_code=status.HTTP_200_OK, response_model=DeleteMenuRespone)
async def delete_menu(menu_id:int):
    try:
        rowcount = await repo.delete_menu(menu_id)
        if rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {menu_id} not found"
            )

        return DeleteMenuRespone(
            message=f"Insert menu id {menu_id} successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
