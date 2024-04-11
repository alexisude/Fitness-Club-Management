-- -- DROP TABLE IF EXISTS Payments;
-- -- DROP TABLE IF EXISTS EquipmentMaintenance;
-- -- DROP TABLE IF EXISTS trainingSessionParticipants;
-- -- DROP TABLE IF EXISTS groupClassParticipants;
-- -- DROP TABLE IF EXISTS sessions;
-- -- DROP TABLE IF EXISTS admins;
-- -- DROP TABLE IF EXISTS trainers;
-- -- DROP TABLE IF EXISTS members;
-- -- Create members table
-- CREATE TABLE members (
--     id SERIAL PRIMARY KEY,
-- 	first_name VARCHAR(255) NOT NULL,
-- 	last_name VARCHAR(255) NOT NULL,
--     height FLOAT,
--     weight FLOAT,
-- 	monthlyFeePaid BOOLEAN,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password VARCHAR(255) NOT NULL
-- );

-- CREATE TABLE exerciseRoutine (
--     id SERIAL PRIMARY KEY,
-- 	memberId INT NOT NULL,
-- 	routineDetails TEXT NOT NULL,
-- 	FOREIGN KEY (memberId) REFERENCES members(id) 
	
-- );

-- CREATE TABLE goals (
--     id SERIAL PRIMARY KEY,
--     memberId INT NOT NULL,
--     goalType VARCHAR(255) NOT NULL,
--     goalValue VARCHAR(255) NOT NULL,
--     goalDate DATE NOT NULL,
-- 	achieved BOOLEAN,
--     FOREIGN KEY (memberId) REFERENCES members(id)  
-- );

-- CREATE TABLE trainers (
--     id SERIAL PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     email VARCHAR(100) NOT NULL,
-- 	password VARCHAR(255) NOT NULL
-- );

-- CREATE TABLE sessions (
--     id SERIAL PRIMARY KEY,
--     trainerId INT NOT NULL,
--     roomNumber INT NOT NULL,
-- 	sessionType TEXT NOT NULL,
--     sessionDate DATE NOT NULL,
--     sessionTime TIME NOT NULL,
--     FOREIGN KEY (trainerId) REFERENCES trainers(id)
-- );


-- CREATE TABLE trainingSessionParticipants (
--     participant_id SERIAL PRIMARY KEY,
--     memberId INT NOT NULL,
--     sessionId INT NOT NULL,
--     FOREIGN KEY (memberId) REFERENCES members(id),
--     FOREIGN KEY (sessionId) REFERENCES sessions(id)
-- );

-- CREATE TABLE groupClassParticipants (
--     participant_id SERIAL PRIMARY KEY,
--     memberId INT NOT NULL,
--     sessionId INT NOT NULL,
--     FOREIGN KEY (memberId) REFERENCES members(id),
--     FOREIGN KEY (sessionId) REFERENCES sessions(id)
-- );


-- CREATE TABLE payments (
--     id SERIAL PRIMARY KEY,
--     member_id INT NOT NULL,
--     amount NUMERIC(10, 2) NOT NULL,
--     payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
--     FOREIGN KEY (member_id) REFERENCES members(id)
-- );

-- CREATE TABLE admins (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(100) NOT NULL UNIQUE,
--     password VARCHAR(255) NOT NULL
-- );
-- CREATE TABLE rooms (
--     id SERIAL PRIMARY KEY,
--     room_number INT NOT NULL UNIQUE,
--     available BOOLEAN NOT NULL DEFAULT TRUE
-- );
-- CREATE TABLE equipment (
--     id SERIAL PRIMARY KEY,
--     equipment_name TEXT NOT NULL,
--     last_maintenance_date DATE DEFAULT CURRENT_DATE
-- 	);
-- CREATE TABLE memberNotifications (
--     id SERIAL PRIMARY KEY,
--     member_id INT NOT NULL,
--     message TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE trainerNotifications (
--     id SERIAL PRIMARY KEY,
--     trainer_id INT NOT NULL,
--     message TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
-- CREATE TABLE admin_bookings (
--     booking_id SERIAL PRIMARY KEY,
--     room_number INT NOT NULL,
--     booking_date DATE NOT NULL
-- );
SELECT * FROM admin_bookings  
-- SELECT * FROM sessions  