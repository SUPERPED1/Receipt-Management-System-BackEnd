import app.db.sql_connector as db

async def get_all_menus():
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT id AS menu_id, base_menu_text AS menu_text, addon_type
                FROM menu_list
            """
            await cur.execute(query)
            result = await cur.fetchall()
    
    return result

async def get_default_menu():
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = """
                SELECT id AS menu_id, base_menu_text AS menu_text, addon_type
                FROM menu_list
                WHERE is_default = 1
                ORDER BY display_order ASC
            """
            await cur.execute(query)
            result = await cur.fetchall()
    
    return result

async def insert_menu(text, addon_type):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            insert_query = """
                INSERT INTO menu_list (base_menu_text, addon_type, display_order)
                VALUES (%s, %s, %s);
            """
            await cur.execute(insert_query, (text, addon_type, 0))
            new_id = cur.lastrowid
            await conn.commit()
    
    return new_id

async def update_default_menu(update_list:list):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                clear_query = """
                    UPDATE menu_list
                    SET is_default = 0, display_order = 0
                    WHERE is_default = 1
                """
                await cur.execute(clear_query)

                update_query = """
                    UPDATE menu_list
                    SET is_default = 1, display_order = %s
                    WHERE id = %s
                """
                await cur.executemany(update_query, update_list)
                await conn.commit()
            except:
                await conn.rollback()
                raise


async def delete_menu(menu_id):
    async with db.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            delete_query = """
                DELETE FROM menu_list
                WHERE id = %s
            """
            await cur.execute(delete_query, (menu_id, ))
            rowcount = cur.rowcount                
            await conn.commit()
    
    return rowcount