import app.core.db_connect as db

async def get_all_customers():
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT company_id, company_name
                FROM customers
                WHERE is_active = 1
            """
            await cur.execute(query)
            result = await cur.fetchall()

    return result