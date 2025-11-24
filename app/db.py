import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Connect to db using credentials in .env file
def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD")
    )
    
    
def getAllMembers():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT member_id, full_name, email FROM members ORDER BY member_id;")
        return cur.fetchall()


def addMember(full_name, email, date_of_birth=None, gender=None, phone=None):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO members (full_name, email, date_of_birth, gender, phone)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING member_id;
                    """, (full_name, email, date_of_birth, gender, phone))
        conn.commit()
        return cur.fetchone()[0] 


def getMemberByEmail(email):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT member_id, full_name, email, date_of_birth, gender, phone, fitness_goal 
                    FROM members 
                    WHERE email = %s;
                    """, (email,))
        return cur.fetchone()
    

def addHealthMetric(member_id, metric_type, metric_value):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO health_metrics (member_id, metric_type, metric_value)
                    VALUES (%s, %s, %s)
                    RETURNING metric_id;
                    """, (member_id, metric_type, metric_value))
        conn.commit()
        return cur.fetchone()[0] 
    

def getMetricsForMember(member_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT metric_id, metric_type, metric_value, recorded_at 
                    FROM health_metrics
                    WHERE member_id = %s
                    ORDER BY recorded_at DESC;
                    """, (member_id,))
        return cur.fetchall()
    

def updateMemberProfile(member_id, full_name, email, date_of_birth, gender, phone, fitness_goal):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    UPDATE members 
                    SET full_name = %s,
                        email = %s, 
                        date_of_birth = %s,
                        gender = %s,
                        phone = %s,
                        fitness_goal = %s
                    WHERE member_id = %s
                    """, (full_name, email, date_of_birth, gender, phone, fitness_goal, member_id))
        conn.commit()
        return cur.rowcount
    
