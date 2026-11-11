from app.core.db_connect import get_database_connection

def get_menu(menu_id:int):
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)
            query = """
                SELECT id AS menu_id, text AS menu_text
                FROM menu
                WHERE id = %s
            """
            cur.execute(query, (menu_id,))
            result = cur.fetchone()
    
            return result
        except:
            raise

def get_menus():
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)
            query = """
                SELECT id AS menu_id, text AS menu_text
                FROM menu
            """
            cur.execute(query)
            result = cur.fetchall()
    
            return result
        except:
            raise

def get_default_menu():
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)
            query = """
                SELECT m.id as menu_id, m.text as menu_text, dm.menu_order
                FROM default_menu as dm
                JOIN menu as m ON m.id = dm.menu_id
                ORDER BY dm.menu_order ASC
            """
            cur.execute(query)
            result = cur.fetchall()
            return result
        except:
            raise

def insert_menu(menu_text):
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)
            insert_query = """
                INSERT INTO menu (text)
                VALUES (%s);
            """
            cur.execute(insert_query, (menu_text,))
            new_id = cur.lastrowid
            query = """
                SELECT id AS menu_id, text AS menu_text
                FROM menu
                WHERE id = %s
            """
            cur.execute(query, (new_id,))
            result = cur.fetchone()
            conn.commit()
    
            return result
        except:
            conn.rollback()
            raise
        
def update_menu(menu_id, menu_text):
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)
            update_query = """
                UPDATE menu 
                SET text = %s
                WHERE id = %s;
            """
            cur.execute(update_query, (menu_text, menu_id))
            query = """
                SELECT id AS menu_id, text AS menu_text
                FROM menu
                WHERE id = %s
            """
            cur.execute(query, (menu_id,))
            result = cur.fetchone()
            conn.commit()
    
            return result
        except:
            conn.rollback()
            raise
        
def delete_menu(menu_id):
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)
            delete_query = """
                DELETE FROM menu
                WHERE id = %s
            """
            cur.execute(delete_query, (menu_id, ))             
            conn.commit()
        except:
            conn.rollback()
            raise

def update_default_menu(update_list:list):
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)

            clear_query = """
                DELETE FROM default_menu;
            """
            cur.execute(clear_query)
            
            update_query = """
                INSERT INTO default_menu (menu_id, menu_order)
                VALUES (%(menu_id)s, %(menu_order)s)
            """
            cur.executemany(update_query, update_list)
            
            query = """
                SELECT m.id as menu_id, m.text as menu_text, dm.menu_order
                FROM default_menu as dm
                JOIN menu as m ON m.id = dm.menu_id
                ORDER BY dm.menu_order ASC
            """
            cur.execute(query)
            result = cur.fetchall()
            conn.commit()
            
            return result
        except:
            conn.rollback()
            raise


