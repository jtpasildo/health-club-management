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