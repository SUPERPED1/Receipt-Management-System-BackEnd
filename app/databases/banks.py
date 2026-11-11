from app.core.db_connect import get_database_connection
from app.error import *

def get_bank(bank_id):
    with get_database_connection() as conn:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT 
                id AS bank_id,
                bank_name,
                branch,
                bank_account,
                owner_name,
                owner_surname,
                limit_used,
                color
            FROM bank_account
            WHERE id = %s
        """
        cur.execute(query, (bank_id,))
        result = cur.fetchone()
    
    return result

def get_all_banks():
    with get_database_connection() as conn:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT 
                id AS bank_id,
                bank_name,
                branch,
                bank_account,
                owner_name,
                owner_surname,
                limit_used,
                color
            FROM bank_account
        """
        cur.execute(query)
        result = cur.fetchall()
    
    return result

def insert_bank(bank_name, branch, bank_account, owner_name, owner_surname, limit_used, color):
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)
            insert_query = """
                INSERT INTO bank_account (bank_name, branch, bank_account, owner_name, owner_surname, limit_used, color)
                VALUES (%s,%s,%s,%s,%s,%s,%s);
            """
            cur.execute(insert_query, (bank_name, branch, bank_account, owner_name, owner_surname, limit_used, color))
        
            new_id = cur.lastrowid
            
            query = """
                SELECT 
                    id AS bank_id,
                    bank_name,
                    branch,
                    bank_account,
                    owner_name,
                    owner_surname,
                    limit_used,
                    color
                FROM bank_account
                WHERE id = %s
            """
            cur.execute(query, (new_id,))
            result = cur.fetchone()
            
            conn.commit()
            return result
        except:    
            conn.rollback()
            raise
        # Adding dup error

def update_bank(bank_id, bank_name, branch, bank_account, owner_name, owner_surname, limit_used, color):
    with get_database_connection() as conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT bank_name
                FROM bank_account
                WHERE id = %s
                """,
                (bank_id,)
            )
            bank = cur.fetchone()
            if not bank:
                raise NotFoundError("Bank not found")
            
            update_query = """
                UPDATE bank_account 
                SET bank_name = %s, branch = %s, bank_account = %s, owner_name = %s, owner_surname = %s, limit_used = %s, color = %s
                WHERE id = %s;
            """
            cur.execute(update_query, (bank_name, branch, bank_account, owner_name, owner_surname, limit_used, color, bank_id))
                    
            query = """
                SELECT 
                    id AS bank_id,
                    bank_name,
                    branch,
                    bank_account,
                    owner_name,
                    owner_surname,
                    limit_used,
                    color
                FROM bank_account
                WHERE id = %s
            """
            cur.execute(query, (bank_id,))
            result = cur.fetchone()
            
            conn.commit()
            return result
        except:    
            conn.rollback()
            raise
        # Adding dup error
      
        
def delete_bank(bank_id:int):
    with get_database_connection() as conn:
        try:
            cur = conn.cursor()
            delete_query = """
                DELETE FROM bank_account
                WHERE id = %s;
            """
            cur.execute(delete_query, (bank_id, ))
            conn.commit()
            return True
        except:
            conn.rollback()
            raise
