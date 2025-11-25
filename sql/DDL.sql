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

DROP TABLE IF EXISTS health_metrics;

CREATE TABLE health_metrics (
	metric_id		SERIAL PRIMARY KEY,
	member_id		INTEGER NOT NULL REFERENCES members(member_id) ON DELETE CASCADE,
	metric_type		VARCHAR(50) NOT NULL,
	metric_value	NUMERIC(10, 2) NOT NULL,
	recorded_at		TIMESTAMP NOT NULL DEFAULT NOW()
);

DROP TABLE IF EXISTS class_registrations;
DROP TABLE IF EXISTS classes;

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


DROP TABLE IF EXISTS trainer_availability;
DROP TABLE IF EXISTS trainers;


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

DROP TABLE IF EXISTS room_bookings;
DROP TABLE IF EXISTS rooms;


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




CREATE TABLE IF NOT EXISTS equipment (
    equipment_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    room_id INTEGER REFERENCES rooms(room_id)
);

CREATE TABLE IF NOT EXISTS maintenance_logs (
    log_id SERIAL PRIMARY KEY,
    equipment_id INTEGER REFERENCES equipment(equipment_id) ON DELETE CASCADE,
    issue TEXT NOT NULL,
    reported_at TIMESTAMP DEFAULT NOW(),
    resolved BOOLEAN DEFAULT FALSE
);


