from psycopg_pool import ConnectionPool
import os


__pool = ConnectionPool(os.getenv('DATABASE_URL'),min_size=1,max_size=10)
    
def exec_db(query,params = None, *,fetch=False):
    with __pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,params=params)
            return cursor.fetchall() if fetch else None

if __name__ == '__main__':
    
    pass
            
        