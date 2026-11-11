import app.core.db_connect as db

async def get_all_companies():
    async with db.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = """
                    SELECT id AS company_id, company_name
                    FROM companies
                    WHERE is_active = 1
                """
                await cur.execute(query)
                result = await cur.fetchall()
    return result

async def insert_company(company, logo_path):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            insert_query = """
                INSERT INTO companies (company_id, company_name, prefix, logo_path, company_detail)
                VALUES (%s, %s, %s, %s ,%s)
            """
            await cur.execute(insert_query, (company.company_id, company.company_name, company.prefix, logo_path, company.company_detail))
            await conn.commit()

async def delete_company(company_id):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            delete_query = """
                DELETE FROM companies
                WHERE company_id = %s
            """
            await cur.execute(delete_query, (company_id, ))
            rowcount = cur.rowcount
            await conn.commit()
    return rowcount
