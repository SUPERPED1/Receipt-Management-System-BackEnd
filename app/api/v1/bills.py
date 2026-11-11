# from fastapi import APIRouter, HTTPException,status, Response
# from app.schemas import CreateBill, BillResponse, BillNumberRespone, BillSummary
# import app.repositories as repo
# import math
# from aiomysql import IntegrityError
# from app.service.pdf_generate.pdfgen import generate_html

# router = APIRouter(prefix="/v1/bills",
#                    tags=["Bills"])

# @router.get("", status_code=status.HTTP_200_OK, response_model=BillResponse)
# async def get_bills(search:str):
#     bills, total = await repo.get_all_bills(search)
    
#     return BillResponse(
#         message="Query bills successfully",
#         total=total["Total"],
#         num_page=math.ceil(total["Total"]/10),
#         bill_list=bills
#     )
    
# @router.get("/total", status_code=status.HTTP_200_OK, response_model=BillSummary)
# async def get_total(month:int, year:int):
#     summary = await repo.get_total(month, year)
    
#     return BillSummary(
#         total=summary["total"],
#         number_bills= summary["number_bills"],
#         paid= summary["paid"],
#         unpaid= summary["unpaid"],
#         number_paid= summary["number_paid"],
#         number_unpaid= summary["number_unpaid"] 
#     )

# @router.get("/next-number", status_code=status.HTTP_200_OK, response_model=BillNumberRespone)
# async def get_last_bill(
#     for_company: str,
#     year: int,
#     month: int
# ):
#     result = await repo.get_last_number(for_company, year, month)
#     if result["last_bill_number"]:
#         present_number = result["last_bill_number"] + 1
#     else:
#         present_number = 1

#     if result["prefix"]:
#         prefix = result["prefix"]
#     else:
#         prefix = "IV"
    
#     receipt_id = f"{prefix}-{year:02d}{month:02d}{present_number:03d}"
#     return BillNumberRespone(
#         message="Query bills successfully",
#         receipt_id=receipt_id
#     )

# @router.post("")
# async def create_bill(payload:CreateBill):
#     try:
#         UUID = await repo.create_bill(payload)

#         return {"messsage":" Insert success", "id":UUID}
#     except IntegrityError:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @router.patch("")
# async def update_bill_status():
#     pass

# @router.get("/download")
# async def download_pdf(id:str):
#     try:
#         data = await repo.print_receipt(id)
#         pdf = await generate_html(data)

#         return Response(
#             pdf,
#             media_type="application/pdf",
#             headers={"Content-Disposition": "inline; filename=output.pdf"}
#         )
#     except Exception as e:
#         raise e