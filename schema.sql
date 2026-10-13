-- ============================================================
-- Department of Computer Science & Engineering — database schema
-- Import this in MySQL Workbench, or run:
--   mysql -u root -p < schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS cs_department
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE cs_department;

-- ---------- Students (registered users) ----------
CREATE TABLE IF NOT EXISTS students (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  full_name     VARCHAR(120)  NOT NULL,
  roll_no       VARCHAR(40)   NOT NULL UNIQUE,
  email         VARCHAR(190)  NOT NULL UNIQUE,
  password_hash VARCHAR(255)  NOT NULL,
  created_at    TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------- Faculty directory ----------
CREATE TABLE IF NOT EXISTS faculty (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(120)  NOT NULL,
  designation   VARCHAR(120)  NOT NULL,
  qualification VARCHAR(160),
  email         VARCHAR(190),
  sort_order    INT DEFAULT 0
) ENGINE=InnoDB;

-- ---------- Notifications / announcements ----------
CREATE TABLE IF NOT EXISTS notifications (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  title         VARCHAR(200)  NOT NULL,
  body          VARCHAR(500),
  posted_on     DATE          NOT NULL,
  is_important  TINYINT(1)    DEFAULT 0
) ENGINE=InnoDB;

-- ---------- Events (seminars, fests, guest lectures) ----------
CREATE TABLE IF NOT EXISTS events (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  title         VARCHAR(200)  NOT NULL,
  description   VARCHAR(500),
  event_date    DATE          NOT NULL,
  location      VARCHAR(160),
  category      VARCHAR(60)
) ENGINE=InnoDB;

-- ---------- Activities (workshops, club initiatives) ----------
CREATE TABLE IF NOT EXISTS activities (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  title         VARCHAR(200)  NOT NULL,
  description   VARCHAR(500),
  activity_date DATE          NOT NULL,
  category      VARCHAR(60)
) ENGINE=InnoDB;


-- ============================================================
-- Seed data — so the site has content to show immediately.
-- Feel free to edit/replace these rows with your real department's data.
-- ============================================================

INSERT INTO faculty (name, designation, qualification, email, sort_order) VALUES
('Dr. R. Sharma',   'Head of Department',      'Ph.D. Computer Science, IIT Delhi',        'r.sharma@sit.edu.in',   1),
('Dr. Anjali Mehta', 'Professor',               'Ph.D. Artificial Intelligence, IISc',      'a.mehta@sit.edu.in',    2),
('Prof. Karan Vora', 'Associate Professor',     'M.Tech Computer Networks, NIT Surat',      'k.vora@sit.edu.in',     3),
('Dr. Sana Iyer',    'Assistant Professor',     'Ph.D. Data Science, IIT Bombay',           's.iyer@sit.edu.in',     4),
('Prof. Arjun Nair', 'Assistant Professor',     'M.Tech Software Engineering, BITS Pilani', 'a.nair@sit.edu.in',     5);

INSERT INTO notifications (title, body, posted_on, is_important) VALUES
('End-semester exam datesheet released', 'The datesheet for the end-semester examinations has been published. Check the department notice board for your slot.', '2026-08-28', 1),
('Guest lecture on Distributed Systems', 'A guest lecture by an industry engineer on distributed systems design will be held on the 10th.', '2026-08-25', 0),
('Lab reallocation for AI/ML batch', 'AI/ML lab sessions for third-year students have moved to Lab 4 starting next week.', '2026-08-20', 0),
('Placement drive registrations open', 'Registrations for the upcoming campus placement drive are now open. Submit your resume by the 15th.', '2026-08-15', 1),
('Library timings extended for exams', 'The department library will remain open until 9 PM during the examination period.', '2026-08-10', 0),
('Hackathon team registration deadline', 'Teams for the annual 24-hour hackathon must register by the end of this week.', '2026-08-05', 0);

INSERT INTO events (title, description, event_date, location, category) VALUES
('TechFest 2026',                  'Annual technical festival featuring coding contests, robotics, and project exhibitions.', '2026-09-20', 'Main Auditorium',      'Fest'),
('Guest Lecture: Cloud Architecture', 'Talk by a senior cloud architect on scalable system design.',                           '2026-09-10', 'Seminar Hall 2',       'Lecture'),
('Alumni Meet 2026',                'An evening to reconnect with department alumni across batches.',                        '2026-10-05', 'Department Courtyard', 'Alumni'),
('Workshop: Intro to Docker & Kubernetes', 'Hands-on workshop on containerization basics for second-year students.',           '2026-07-15', 'Lab 3',                'Workshop'),
('National Coding Championship (Round 1)', 'Department-level qualifiers for the national coding championship.',               '2026-06-30', 'Computer Lab 1',       'Competition');

INSERT INTO activities (title, description, activity_date, category) VALUES
('Weekend DSA Bootcamp', 'A 3-day intensive bootcamp on data structures and algorithms run by the coding club.', '2026-08-22', 'Workshop'),
('Open Source Contribution Drive', 'Students contributed to five open-source projects as part of a department-wide initiative.', '2026-08-01', 'Club Activity'),
('Robotics Club Demo Day', 'The robotics club showcased four student-built projects to first-year students.', '2026-07-18', 'Showcase'),
('Paper Publication: IEEE Conference', 'Two final-year students published a research paper at a regional IEEE conference.', '2026-06-10', 'Research');
