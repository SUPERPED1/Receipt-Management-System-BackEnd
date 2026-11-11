# from fastapi import APIRouter, HTTPException, status
# from app.schemas import CustomerRespone
# import app.repositories as repo

# router = APIRouter(prefix="/v1/customers",
#                    tags=["Customers"])

# @router.get("", status_code=status.HTTP_200_OK, response_model=CustomerRespone)
# async def get_customers():
#     try:
#         customers = await repo.get_all_customers()
                
#         return CustomerRespone(
#             message = "Query success",
#             customer_list = customers
#         )
#     except Exception as e:
#         #logger.warning()
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    