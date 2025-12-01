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
    

def getAllClasses():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT class_id, class_name, class_time, capacity FROM classes ORDER BY class_time;
                    """)
        return cur.fetchall()

def countRegistrations(class_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT COUNT(*) FROM class_registrations WHERE class_id = %s;
                    """, (class_id,))
        return cur.fetchone()[0] 
    
def registerForClass(member_id, class_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO class_registrations (member_id, class_id)
                    VALUES (%s, %s)
                    ON CONFLICT (member_id, class_id) DO NOTHING
                    RETURNING registration_id;
                    """, (member_id, class_id))
        conn.commit()
        return cur.fetchone()
    
##TRAINER
def getTrainerByEmail(email):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT trainer_id, full_name, email
                    FROM trainers 
                    WHERE email = %s;
                    """, (email,))
        return cur.fetchone()
    
def addTrainerAvailability(trainer_id, start_time, end_time):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO trainer_availability (trainer_id, start_time, end_time)
                    VALUES (%s, %s, %s)
                    RETURNING availability_id;
                    """, (trainer_id, start_time, end_time))
        conn.commit()
        return cur.fetchone()[0] 
    
def getAvailabilityForTrainer(trainer_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT availability_id, start_time, end_time
                    FROM trainer_availability
                    WHERE trainer_id = %s
                    ORDER BY start_time;
                    """, (trainer_id,))
        return cur.fetchall()
    
def searchMembersByName(name_query):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT member_id, full_name, email, fitness_goal 
                    FROM members 
                    WHERE LOWER(full_name) LIKE LOWER(%s)
                    ORDER BY full_name;
                    """, (f"%{name_query}%",))
        return cur.fetchall()

def getLatestMetric(member_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT metric_type, metric_value, recorded_at
                    FROM health_metrics
                    WHERE member_id = %s
                    ORDER BY recorded_at DESC
                    LIMIT 1;
                    """, (member_id,))
        return cur.fetchone()
    
    
def getAllRooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT room_id, room_name
                    FROM rooms 
                    ORDER BY room_id;
                    """)
        return cur.fetchall() 
    
def getBookingsForRoom(room_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT booking_id, class_id, start_time, end_time
                    FROM room_bookings
                    WHERE room_id = %s
                    ORDER BY start_time;
                    """, (room_id,))
        return cur.fetchall()
    
def createRoomBooking(room_id, class_id, start_time, end_time):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO room_bookings (room_id, class_id, start_time, end_time)
                    VALUES (%s, %s, %s, %s)
                    RETURNING booking_id;
                    """, (room_id, class_id, start_time, end_time))
        conn.commit()
        return cur.fetchone()[0]
    

def getAllEquipment():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT e.equipment_id, 
                           e.name,
                           r.room_name
                    FROM equipment e
                    LEFT JOIN rooms r ON e.room_id = r.room_id 
                    ORDER BY e.equipment_id;
                    """)
        return cur.fetchall()
    
def addEquipment(name, room_id=None):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO equipment (name, room_id)
                    VALUES (%s, %s)
                    RETURNING equipment_id;
                    """, (name, room_id))
        conn.commit()
        return cur.fetchone()[0] 

def reportEquipmentIssue(equipment_id, issue):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO maintenance_logs (equipment_id, issue)
                    VALUES (%s, %s)
                    RETURNING log_id;
                    """, (equipment_id, issue))
        conn.commit()
        return cur.fetchone()[0] 
    
def getOpenIssues():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT ml.log_id, 
                           e.equipment_id,
                           e.name,
                           ml.issue,
                           ml.reported_at
                    FROM maintenance_logs ml
                    JOIN equipment e ON ml.equipment_id = e.equipment_id
                    WHERE ml.resolved = FALSE
                    ORDER BY ml.reported_at;
                    """)
        return cur.fetchall()
    
def resolveIssue(log_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    UPDATE maintenance_logs
                    SET resolved = TRUE
                    WHERE log_id = %s;
                    """, (log_id,))
        conn.commit()
        return cur.rowcount