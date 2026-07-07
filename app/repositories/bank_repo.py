import app.db.sql_connector as db
from app.schemas import CreateBank

async def get_all_banks():
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT id AS bank_id, bank_name, owner_name
                FROM bank_account
                WHERE is_active = 1
            """
            await cur.execute(query)
            result = await cur.fetchall()
    
    return result

async def insert_bank(payload:CreateBank):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            insert_query = """
                INSERT INTO bank_account (bank_name, bank_branch, bank_account_id, owner_name, owner_surname, color_display)
                VALUES (%s,%s,%s,%s,%s,%s);
            """
            await cur.execute(insert_query, (payload.bank_name, payload.bank_branch, payload.bank_account_id, payload.owner_name, payload.owner_surname, payload.color_display))
            new_id = cur.lastrowid
            await conn.commit()
    
    return new_id

async def delete_bank(bank_id:int):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            delete_query = """
                DELETE FROM bank_account
                WHERE id = %s;
            """
            await cur.execute(delete_query, (bank_id, ))
            rowcount = cur.rowcount
            await conn.commit()
    
    return rowcount
