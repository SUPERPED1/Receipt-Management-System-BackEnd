from fastapi import APIRouter, HTTPException, status
from app.schemas import BankResponse, CreateBank, CreateBankReaponse, DeleteBankResponse
import app.repositories as repo
from aiomysql import IntegrityError

router = APIRouter(prefix="/v1/banks",
                   tags=["Banks"])

@router.get("", status_code=status.HTTP_200_OK, response_model=BankResponse)
async def get_banks():
    try:
        bank_datas = await repo.get_all_banks()
        
        return BankResponse(
            message="Query banks successfully",
            bank_list=bank_datas
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateBankReaponse)
async def create_bank(payload:CreateBank):
    try:
        new_id = await repo.insert_bank()

        return CreateBankReaponse(
            message="Insert bank successfully",
            insert_data={
                "bank_id": new_id,
                "bank_name": payload.bank_name,
                "owner_name": payload.owner_name
            }
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# @router.put("", status_code=status.HTTP_200_OK, response_model=BankResponse)
# async def update_bank():
#     try:
#         bank_datas = await repo.get_all_banks()

#         return BankResponse(
#             message="Query banks successfully",
#             bank_list=bank_datas
#         )
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/{bank_id}", status_code=status.HTTP_200_OK, response_model=DeleteBankResponse)
async def delete_bank(bank_id:int):
    try:
        is_delete = await repo.delete_bank()

        if is_delete == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bank {bank_id} not found"
            )

        return DeleteBankResponse(
            message=f"Delete Bank {bank_id} successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)