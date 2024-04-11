INSERT INTO trainers (first_name, last_name, email, password) VALUES
('Alexis', 'Ude', 'alexis@gm.com', '123'),
('CBUM', 'Youtube', 'c@gm.com', '123');

INSERT INTO sessions (trainerId, roomNumber, sessionType, sessionDate, sessionTime) VALUES
(1, 2, 'Personal Training', '2024-04-05', '9:00'),
(1, 4, 'Yoga', '2024-04-04', '16:00'),
(1, 5, 'Zumba', '2024-04-03', '10:00');

INSERT INTO admins (email, password ) VALUES
('admin', '123');

INSERT INTO rooms (room_number, available) VALUES
(1, true),
(2, false),
(3, true),
(4, false),
(5, false),
(6, true),
(7, true),
(8, true),
(9, true),
(10, true);

INSERT INTO equipment (equipment_name, last_maintenance_date) VALUES
('Treadmill', '2024-01-01'),
('Bicep Machine', '2023-01-01'),
('Rowing Machine', '2024-02-01');

