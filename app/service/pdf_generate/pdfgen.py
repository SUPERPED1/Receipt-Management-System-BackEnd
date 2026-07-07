from pathlib import Path
from jinja2 import Template
from playwright.async_api import async_playwright
from pythainlp.util import bahttext
import base64
import app.db.sql_connector as db
import json
import asyncio

async def data_preprocess(payload):
    date = f"{payload["created_on"].day:02d}/{payload["created_on"].month:02d}/{payload["created_on"].year + 543}"
    total = payload["total_price"]
    payload["details"] = json.loads(payload["details"])
    for item in payload["details"]:
        item["price"] = f"{item["price"]:,.2f}"

    empty = 7 - len(payload["details"])

    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT *
                FROM bank_account
                WHERE id = %s
            """
            await cur.execute(query, (payload["bank_id"],))
            result = await cur.fetchone()

    return {
        "to_company": payload["customer_name"],
        "receipt_id": payload["bill_id"],
        "date": date,
        "listItem": payload["details"],
        "total_text": bahttext(total),
        "total": f"{total:,.2f}",
        "empty": empty,
        "bank_detail": result
    }


async def generate_html(payload):
    if payload["for_company"] == "1":
        path = Path(r"D:\Every_file\receipt\Receipt_print_project\backend\app\service\pdf_generate\template\skall.html")
        template_path = r"D:/Every_file/receipt/Receipt_print_project/backend/app/service/pdf_generate/template/logo.png"
    else:
        path = Path(r"D:\Every_file\receipt\Receipt_print_project\backend\app\service\pdf_generate\template\acpro.html")
        template_path = r"D:/Every_file/receipt/Receipt_print_project/backend/app/service/pdf_generate/template/S.png"

    # Read HTML and image concurrently
    html, logo_bytes = await asyncio.gather(
        asyncio.to_thread(path.read_text, encoding="utf-8"),
        asyncio.to_thread(_read_file_bytes, template_path),
    )

    base64_logo = base64.b64encode(logo_bytes).decode()
    LOGO_PATH = f"data:image/png;base64,{base64_logo}"

    template = Template(html)
    pre_data = await data_preprocess(payload)

    rendered_html = template.render(
        to_company=pre_data["to_company"],
        receipt_id=pre_data["receipt_id"],
        date=pre_data["date"],
        listItem=pre_data["listItem"],
        total_text=pre_data["total_text"],
        total=pre_data["total"],
        empty=pre_data["empty"],
        bank_detail=pre_data["bank_detail"],
        color=pre_data["bank_detail"]["color_display"],
        logo_path=LOGO_PATH
    )

    pdf = await html_to_pdf(rendered_html)
    return pdf


def _read_file_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


async def html_to_pdf(html: str) -> bytes:
    return await asyncio.to_thread(_run_playwright, html)

# Playwright ใช้ subprocess เพื่อเปิด Chromium ขึ้นมา แต่บน Windows, asyncio default event loop (ProactorEventLoop) มีข้อจำกัดในการ spawn subprocess ภายใน loop ที่รันอยู่แล้ว วิธีนี้จึงแยก Playwright ออกไปรันใน thread pool แทน ซึ่งมี event loop ของตัวเองและไม่มีปัญหานี้
def _run_playwright(html: str) -> bytes:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.set_content(html)
        pdf_bytes = page.pdf(format="A4")
        browser.close()
    return pdf_bytes