DROP TABLE IF EXISTS maintenance_logs;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS room_bookings;
DROP TABLE IF EXISTS trainer_availability;
DROP TABLE IF EXISTS class_registrations;
DROP TABLE IF EXISTS health_metrics;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS members;

CREATE TABLE members (
	member_id		SERIAL PRIMARY KEY,
	full_name		VARCHAR(100) NOT NULL,
	email			VARCHAR(255) NOT NULL UNIQUE,
	date_of_birth	DATE,
	gender			VARCHAR(20),
	phone			VARCHAR(20),
    fitness_goal    VARCHAR(255)
);


CREATE TABLE health_metrics (
	metric_id		SERIAL PRIMARY KEY,
	member_id		INTEGER NOT NULL REFERENCES members(member_id) ON DELETE CASCADE,
	metric_type		VARCHAR(50) NOT NULL,
	metric_value	NUMERIC(10, 2) NOT NULL,
	recorded_at		TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE classes (
    class_id    SERIAL PRIMARY KEY,
    class_name  VARCHAR(100) NOT NULL,
    class_time  TIMESTAMP NOT NULL,
    capacity    INTEGER NOT NULL
);

CREATE TABLE class_registrations (
    registration_id    SERIAL PRIMARY KEY,
    member_id          INTEGER NOT NULL REFERENCES members(member_id) ON DELETE CASCADE,
    class_id           INTEGER NOT NULL REFERENCES classes(class_id) ON DELETE CASCADE,
    registered_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (member_id, class_id)
);



CREATE TABLE trainers (
    trainer_id  SERIAL PRIMARY KEY,
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE trainer_availability (
    availability_id   SERIAL PRIMARY KEY,
    trainer_id        INTEGER NOT NULL REFERENCES trainers(trainer_id) ON DELETE CASCADE,
    start_time        TIMESTAMP NOT NULL,
    end_time          TIMESTAMP NOT NULL,
    CHECK (end_time > start_time)
);


CREATE TABLE rooms (
    room_id  SERIAL PRIMARY KEY,
    room_name   VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE room_bookings (
    booking_id   SERIAL PRIMARY KEY,
    room_id      INTEGER NOT NULL REFERENCES rooms(room_id) ON DELETE CASCADE,
    class_id     INTEGER NOT NULL REFERENCES classes(class_id) ON DELETE CASCADE,
    start_time   TIMESTAMP NOT NULL,
    end_time     TIMESTAMP NOT NULL,
    CHECK (end_time > start_time)
);


CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    room_id INTEGER REFERENCES rooms(room_id)
);


CREATE TABLE maintenance_logs (
    log_id SERIAL PRIMARY KEY,
    equipment_id INTEGER REFERENCES equipment(equipment_id) ON DELETE CASCADE,
    issue TEXT NOT NULL,
    reported_at TIMESTAMP DEFAULT NOW(),
    resolved BOOLEAN DEFAULT FALSE
);

-- INDEX to speed up health metric lookups by member and sort by most recent
CREATE INDEX idx_health_metrics_member_id_recorded_at
    ON health_metrics (member_id, recorded_at);


-- VIEW that returns all unresolved equipment issues with room & equipment
CREATE OR REPLACE VIEW unresolved_equipment_issues AS
SELECT
    ml.log_id,
    e.equipment_id,
    e.name AS equipment_name,
    r.room_name,
    ml.issue,
    ml.reported_at
FROM maintenance_logs ml
JOIN equipment e ON ml.equipment_id = e.equipment_id
LEFT JOIN rooms r ON e.room_id = r.room_id
WHERE ml.resolved = FALSE;


-- TRIGGER function that automatically sets reported_at timestamp if missing
CREATE OR REPLACE FUNCTION set_reported_at()
RETURNS TRIGGER AS $$
BEGIN 
    IF NEW.reported_at is NULL THEN
        NEW.reported_at := NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Remove old TRIGGER if it exists
DROP TRIGGER IF EXISTS trg_set_reported_at ON maintenance_logs;

-- TRIGGER that runs before inserting or updating a maintenance log
-- Ensures every issue has a valid reported_at timestamp
CREATE TRIGGER trg_set_reported_at
BEFORE INSERT OR UPDATE ON maintenance_logs
FOR EACH ROW
EXECUTE FUNCTION set_reported_at();