import app.core.db_connect as db
from app.schemas import CreateBill
import uuid

async def get_last_number(for_company, year, month):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT
                    (SELECT last_bill_number
                    FROM last_bill_check
                    WHERE company_id = %s AND year = %s AND month = %s) AS last_bill_number,
                    (SELECT prefix
                    FROM companies
                    WHERE id = %s) AS prefix
            """
            await cur.execute(query, (for_company, year, month, for_company))
            result = await cur.fetchone()
    
    return result

async def get_total(month, year):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT 
                    SUM(total_price) AS total,
                    COUNT(*) AS number_bills,

                    SUM(CASE WHEN bill_status = 'paid' THEN total_price ELSE 0 END) AS paid,
                    SUM(CASE WHEN bill_status = 'unpaid' THEN total_price ELSE 0 END) AS unpaid,

                    SUM(CASE WHEN bill_status = 'paid' THEN 1 ELSE 0 END) AS number_paid,
                    SUM(CASE WHEN bill_status = 'unpaid' THEN 1 ELSE 0 END) AS number_unpaid

                FROM main_bill
                WHERE billing_month = %s AND billing_year = %s
                AND bill_status <> 'cancel';
            """
            await cur.execute(query, (month,year))
            result = await cur.fetchone()
    
    return result

async def get_all_bills(search):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT m.UUID AS id, m.created_on, m.bill_id, cus.company_name AS customer_name, com.company_name AS for_company, bank.bank_name, bank.owner_name AS bank_owner_name, m.total_price, m.bill_status,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'menu_text', de.item_text,
                            'price', de.unit_price
                        )
                    ) AS bill_detail
                FROM main_bill AS m
                LEFT JOIN customers AS cus ON cus.company_id = m.customer_company_id
                LEFT JOIN companies AS com ON com.id = m.for_company
                LEFT JOIN bank_account AS bank ON bank.id = m.bank_id
                LEFT JOIN detail_bill AS de ON de.bill_UUID = m.UUID
                WHERE m.bill_id LIKE %s OR cus.company_name LIKE %s OR m.customer_company_id LIKE %s
                GROUP BY m.UUID, m.created_on, m.bill_id, cus.company_name, 
                        com.company_name, bank.bank_name, bank.owner_name, 
                        m.total_price, m.bill_status
                ORDER BY m.created_on DESC, m.bill_id DESC
                LIMIT 10;
            """
            await cur.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%"))
            result = await cur.fetchall()
            
            query = """
                SELECT COUNT(UUID) AS Total
                FROM main_bill
            """
            await cur.execute(query)
            total = await cur.fetchone()
            
            await conn.commit()
    
    return result, total

async def create_bill(payload: CreateBill):
    UUID = str(uuid.uuid4())
    total = 0
    insert_item = []
    for item in payload.details:
        insert_item.append((UUID, item.menu_text, item.price))
        total += round(item.price, 2)
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                insert_main_bill = """
                    INSERT INTO main_bill (UUID,billing_month, billing_year, bill_id, customer_company_id, for_company, total_price, bank_id, bill_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                await cur.execute(insert_main_bill, (UUID, payload.monthly, payload.yearly, payload.receipt_id, payload.customer_company_id, payload.for_company, total, payload.bank_id, "unpaid"))

                insert_detail_bill = """
                    INSERT INTO detail_bill (bill_UUID, item_text, unit_price)
                    VALUES (%s,%s,%s)
                """
                await cur.executemany(insert_detail_bill, insert_item)

                upsert_bill_number = """
                    INSERT INTO last_bill_check (company_id, year, month, last_bill_number)
                    VALUES (%s, %s, %s, 1)
                    ON DUPLICATE KEY UPDATE last_bill_number = last_bill_number + 1;
                """
                await cur.execute(upsert_bill_number, (payload.for_company, payload.yearly, payload.monthly))

                await conn.commit()
                
                return UUID

            except Exception as e:
                await conn.rollback()
                raise

async def print_receipt(id):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT m.created_on, m.bill_id, cus.company_name AS customer_name, m.for_company, m.bank_id, m.total_price,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'menu_text', de.item_text,
                            'price', de.unit_price
                        )
                    ) AS details
                FROM main_bill AS m
                LEFT JOIN customers AS cus ON cus.company_id = m.customer_company_id
                LEFT JOIN detail_bill AS de ON de.bill_UUID = m.UUID
                WHERE m.uuid = %s
                GROUP BY m.UUID, m.created_on, m.bill_id, cus.company_name, 
                        m.for_company, m.bank_id, m.total_price, m.bill_status
            """
            await cur.execute(query, (id,))
            result = await cur.fetchone()
    
    return result