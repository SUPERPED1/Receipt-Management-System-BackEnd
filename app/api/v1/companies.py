from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
import app.repositories as repo
from app.schemas import CompanyResponse, CreateCompany, CreateCompanyRespone, DeleteCompanyRespone
from app.service.save_tools.save_file import save_file
from aiomysql import IntegrityError

router = APIRouter(prefix="/v1/companies",
                   tags=["Companies"])

@router.get("", status_code=status.HTTP_200_OK, response_model=CompanyResponse)
async def get_companies():
    try:
        companies = await repo.get_all_companies()

        return CompanyResponse(
            message="Query companies successfully",
            company_list=companies
        )
    except Exception as e:
        raise e
        # raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateCompanyRespone)
async def create_company(
    logo_file:UploadFile = File(...),
    data:str = Form(...,
        description='JSON string: {"companyId":"123","companyName":"ABC","prefix":"Mr.","companyDetail":"..."}')
):
    try:
        logo_path = await save_file(logo_file)
        company = CreateCompany.model_validate_json(data)
        
        await repo.insert_company(company, logo_path)

        return CreateCompanyRespone(
            message="Company created successfully",
            insert_data={
                "company_id":company.company_id,
                "company_name":company.company_name,
                "prefix":company.prefix
            }
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{company_id}", status_code=status.HTTP_200_OK, response_model=DeleteCompanyRespone)
async def delete_company(company_id:str):
    try:
        rowcount = await repo.delete_company(company_id)

        if rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company {company_id} not found"
            )
        
        return DeleteCompanyRespone(
            message=f"Delete company with company id: {company_id} successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            

