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


# MEMBER FUNCTION QUERIES #

# Returns all members    
def getAllMembers():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT member_id, full_name, email FROM members ORDER BY member_id;")
        return cur.fetchall()

# Insert a new member and return the member id
def addMember(full_name, email, date_of_birth=None, gender=None, phone=None):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO members (full_name, email, date_of_birth, gender, phone)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING member_id;
                    """, (full_name, email, date_of_birth, gender, phone))
        conn.commit()
        return cur.fetchone()[0] 

# Look up a member and return full profile details
def getMemberByEmail(email):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT member_id, full_name, email, date_of_birth, gender, phone, fitness_goal 
                    FROM members 
                    WHERE email = %s;
                    """, (email,))
        return cur.fetchone()
    
# Add a new health metric entry for a member
def addHealthMetric(member_id, metric_type, metric_value):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO health_metrics (member_id, metric_type, metric_value)
                    VALUES (%s, %s, %s)
                    RETURNING metric_id;
                    """, (member_id, metric_type, metric_value))
        conn.commit()
        return cur.fetchone()[0] 
    
# Get all health metrics for a memeber, newest first
def getMetricsForMember(member_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT metric_id, metric_type, metric_value, recorded_at 
                    FROM health_metrics
                    WHERE member_id = %s
                    ORDER BY recorded_at DESC;
                    """, (member_id,))
        return cur.fetchall()
    
# Update all profile fields for a memeber
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
    
# Return all classes with time and capacity
def getAllClasses():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT class_id, class_name, class_time, capacity FROM classes ORDER BY class_time;
                    """)
        return cur.fetchall()

# Count how many registrations exist for a given class
def countRegistrations(class_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT COUNT(*) FROM class_registrations WHERE class_id = %s;
                    """, (class_id,))
        return cur.fetchone()[0] 

# Register a member for a class
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
    

# TRAINER FUNCTION QUERIES #

# Look up trainer by email and return id, name, and email
def getTrainerByEmail(email):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT trainer_id, full_name, email
                    FROM trainers 
                    WHERE email = %s;
                    """, (email,))
        return cur.fetchone()

# Add an availability window for a trainer
def addTrainerAvailability(trainer_id, start_time, end_time):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO trainer_availability (trainer_id, start_time, end_time)
                    VALUES (%s, %s, %s)
                    RETURNING availability_id;
                    """, (trainer_id, start_time, end_time))
        conn.commit()
        return cur.fetchone()[0] 

# Get all avalability windows for a trainer    
def getAvailabilityForTrainer(trainer_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT availability_id, start_time, end_time
                    FROM trainer_availability
                    WHERE trainer_id = %s
                    ORDER BY start_time;
                    """, (trainer_id,))
        return cur.fetchall()
    
# Search members by name
def searchMembersByName(name_query):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT member_id, full_name, email, fitness_goal 
                    FROM members 
                    WHERE LOWER(full_name) LIKE LOWER(%s)
                    ORDER BY full_name;
                    """, (f"%{name_query}%",))
        return cur.fetchall()

# Get the latest metric recorded for a member
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
    
# Return all rooms 
def getAllRooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT room_id, room_name
                    FROM rooms 
                    ORDER BY room_id;
                    """)
        return cur.fetchall() 
    
# Get all bookings for a specific room
def getBookingsForRoom(room_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    SELECT booking_id, class_id, start_time, end_time
                    FROM room_bookings
                    WHERE room_id = %s
                    ORDER BY start_time;
                    """, (room_id,))
        return cur.fetchall()
 
# Create a new room booking and return the booking_id   
def createRoomBooking(room_id, class_id, start_time, end_time):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO room_bookings (room_id, class_id, start_time, end_time)
                    VALUES (%s, %s, %s, %s)
                    RETURNING booking_id;
                    """, (room_id, class_id, start_time, end_time))
        conn.commit()
        return cur.fetchone()[0]
    
# Return all equipment with associated room name
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
    
# Add a new piece of equipment and assign it to a room
def addEquipment(name, room_id=None):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO equipment (name, room_id)
                    VALUES (%s, %s)
                    RETURNING equipment_id;
                    """, (name, room_id))
        conn.commit()
        return cur.fetchone()[0] 

# Create a maintenance log entry for an equipment issue
def reportEquipmentIssue(equipment_id, issue):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO maintenance_logs (equipment_id, issue)
                    VALUES (%s, %s)
                    RETURNING log_id;
                    """, (equipment_id, issue))
        conn.commit()
        return cur.fetchone()[0] 

# Return all unresolved maintenance issues with equipment details    
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

# Mark a maintenance log as resolved    
def resolveIssue(log_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
                    UPDATE maintenance_logs
                    SET resolved = TRUE
                    WHERE log_id = %s;
                    """, (log_id,))
        conn.commit()
        return cur.rowcount