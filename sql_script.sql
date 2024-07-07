CREATE DATABASE fitness_center;
USE fitness_center

CREATE TABLE members (
id INT AUTO_INCREMENT PRIMARY KEY,
member_name VARCHAR(75) NOT NULL,
email VARCHAR(100) NOT NULL,
phone VARCHAR(15) NOT NULL,
cc_number INT NOT NULL);

ALTER TABLE members
DROP COLUMN cc_number;


CREATE TABLE workout_sessions (
id INT AUTO_INCREMENT PRIMARY KEY,
member_id INT NOT NULL,
duration INT NOT NULL,
session_time_date DATETIME NOT NULL,
FOREIGN KEY (member_id) REFERENCES members(id));

INSERT INTO members (member_name, email, phone)
VALUES ('Emily Johnson','emily.j@example.net','555-987-6543'),
('Alanis Brown','alanis@mailserver.org','555-246-8135'),
('Sarah Davis','sarahdavis@webmail.com','555-369-2580');

INSERT INTO workout_sessions (member_id, duration, session_time_date)
VALUES (1,1,'2024-07-07 06:00:00'),
(2,2,'2024-07-07 08:00:00');

-- INSERT VALUES
SELECT * FROM members;
SELECT * FROM workout_sessions;





