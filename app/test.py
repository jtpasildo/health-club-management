from db import get_conn

with get_conn() as conn, conn.cursor() as cur:
    cur.execute("SELECT current_database();")
    db_name = cur.fetchone()[0]
    print("Connected to database:", db_name)

    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    print("Public tables:")
    for row in tables:
        print("-", row[0])
