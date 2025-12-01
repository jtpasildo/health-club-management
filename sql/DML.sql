INSERT INTO classes (class_name, class_time, capacity)
VALUES
    ('Morning Yoga', '2025-12-05 09:00', 10),
    ('Spin Class', '2025-12-05 11:00', 8),
    ('Evening HITT', '2025-12-05 18:30', 12);

INSERT INTO trainers (full_name, email)
VALUES
    ('Terry Crews', 'terry.trainer@mail.com'),
    ('Bruce Lee', 'bruce.trainer@mail.com'),
    ('Taylor Swift', 'taylor.trainer@mail.com');

INSERT INTO rooms (room_name) 
VALUES
    ('Studio A'),
    ('Studio B'),
    ('Recovery Room');

----
INSERT INTO members (full_name, email, date_of_birth, gender, phone, fitness_goal) 
VALUES
    ('Bob Sponge', 'bob@mail.com', '1999-05-01', 'Male', '4160000000', 'Build muscle'),
    ('Tim Turner', 'tim@mail.com', '1998-10-04', 'Male', '4161111111', 'General Fitness'),
    ('Dora Explorer', 'dora@mail.com', '1999-05-01', 'Female', '4162222222', 'Improve Cardio');


INSERT INTO health_metrics (member_id, metric_type, metric_value) 
VALUES
    (1, 'weight', 150.0),
    (1, 'body_fat', 25.3),
    (1, 'heart_rate', 72.0);

INSERT INTO class_registrations (member_id, class_id) 
VALUES
    (1, 1),
    (1, 2),
    (2, 2),
    (3, 3);


INSERT INTO trainer_availability (trainer_id, start_time, end_time) 
VALUES
    (1, '2025-11-30 08:00', '2025-11-30 10:00'),
    (2, '2025-12-01 14:00', '2025-12-01 16:00'),
    (3, '2025-12-02 10:00', '2025-12-02 12:00');

INSERT INTO room_bookings (room_id, class_id, start_time, end_time) 
VALUES
    (1, 1, '2025-11-30 06:00', '2025-11-30 07:30'),
    (2, 2, '2025-12-05 11:00', '2025-12-05 12:30'),
    (3, 3, '2025-12-05 18:30', '2025-12-05 19:30');


INSERT INTO equipment (name, room_id) 
VALUES
    ('Squat Rack', 1),
    ('Bench', 2),
    ('Sauna', 3);

INSERT INTO maintenance_logs (equipment_id, issue, resolved) 
VALUES
    (1, 'Unable to adjust height', FALSE),
    (2, 'Will not recline back', FALSE),
    (3, 'Not turning off', FALSE);