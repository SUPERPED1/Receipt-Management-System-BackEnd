from fastapi import APIRouter, HTTPException, status
import app.schemas as schema
from app.error import *
import app.databases.banks as db
from aiomysql import IntegrityError

router = APIRouter(prefix="/v1/banks",
                   tags=["Banks"])

@router.get("/{bank_id}", status_code=status.HTTP_200_OK, 
            response_model=schema.Response[schema.banks.Bank])
async def get_bank(bank_id):
    try:
        bank_data = db.get_bank(bank_id)
        
        if not bank_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
        
        return schema.Response(
            data = bank_data
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("", status_code=status.HTTP_200_OK, response_model=schema.ListResponse[schema.banks.Bank])
def get_banks():
    try:
        bank_datas = db.get_all_banks()
        
        return schema.ListResponse(
            data=bank_datas
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schema.CreateResponse[schema.banks.Bank])
async def create_bank(payload:schema.banks.CreateBank):
    try:
        new_bank = db.insert_bank(payload.bank_name, payload.branch, payload.bank_account, payload.owner_name, payload.owner_surname, payload.limit_used, payload.color)

        return schema.CreateResponse(
            data = new_bank
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Banks already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.patch("/{bank_id}", status_code=status.HTTP_200_OK, response_model=schema.UpdateResponse[schema.banks.Bank])
async def update_bank(bank_id:int, payload:schema.banks.UpdateBank):
    try:
        updated_bank = db.update_bank(bank_id, payload.bank_name, payload.branch, payload.bank_account, payload.owner_name, payload.owner_surname, payload.limit_used, payload.color)

        return schema.UpdateResponse(
            data = updated_bank
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/{bank_id}", status_code=status.HTTP_200_OK, response_model=schema.DeleteResponse)
async def delete_bank(bank_id:int, confirm_text):
    try:
        result = db.get_bank(bank_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
        
        text = f"ลบ {result['bank_account']}"
        if confirm_text != text:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmation text does not match")  
              
        db.delete_bank(bank_id)

        return schema.DeleteResponse(data=None)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)