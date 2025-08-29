-- Drop tables if they exist (for fresh start)
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS attendees CASCADE;
DROP TABLE IF EXISTS organizers CASCADE;

-- Create Organizers table
CREATE TABLE organizers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    organizer_id INTEGER REFERENCES organizers(id) ON DELETE CASCADE
);

-- Create Attendees table
CREATE TABLE attendees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Tickets table (many-to-many relationship)
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    attendee_id INTEGER REFERENCES attendees(id) ON DELETE CASCADE,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, attendee_id)
);

-- Insert Organizers
INSERT INTO organizers (name, email, phone) VALUES
('John Smith', 'john@email.com', '+1234567890'),
('Sarah Johnson', 'sarah@email.com', '+1234567891'),
('Mike Wilson', 'mike@email.com', '+1234567892'),
('Emily Brown', 'emily@email.com', '+1234567893'),
('David Davis', 'david@email.com', '+1234567894'),
('Lisa Garcia', 'lisa@email.com', '+1234567895'),
('Tom Martinez', 'tom@email.com', '+1234567896'),
('Anna Taylor', 'anna@email.com', '+1234567897'),
('Chris Anderson', 'chris@email.com', '+1234567898'),
('Maria Rodriguez', 'maria@email.com', '+1234567899');

-- Insert Events
INSERT INTO events (name, date, location, description, organizer_id) VALUES
('Tech Conference 2024', '2024-12-15', 'San Francisco, CA', 'Annual technology conference featuring the latest innovations', 1),
('Music Festival', '2024-11-20', 'Austin, TX', 'Three-day music festival with top artists', 2),
('Business Summit', '2024-12-05', 'New York, NY', 'Networking event for business professionals', 3),
('Art Exhibition', '2024-11-30', 'Los Angeles, CA', 'Contemporary art exhibition by emerging artists', 4),
('Food & Wine Festival', '2024-12-10', 'Portland, OR', 'Celebration of local cuisine and wines', 5),
('Marathon 2024', '2024-11-25', 'Chicago, IL', 'Annual city marathon for all skill levels', 6),
('Book Fair', '2024-12-01', 'Seattle, WA', 'Independent authors and publishers showcase', 7),
('Gaming Convention', '2024-11-28', 'Las Vegas, NV', 'Gaming enthusiasts convention with competitions', 8),
('Science Fair', '2024-12-08', 'Boston, MA', 'Student science projects and demonstrations', 9),
('Fashion Week', '2024-12-12', 'Miami, FL', 'Latest fashion trends and designer showcases', 10);

-- Insert Attendees
INSERT INTO attendees (name, email, phone) VALUES
('Alice Cooper', 'alice@email.com', '+1111111111'),
('Bob Miller', 'bob@email.com', '+2222222222'),
('Carol White', 'carol@email.com', '+3333333333'),
('Daniel Lee', 'daniel@email.com', '+4444444444'),
('Emma Wilson', 'emma@email.com', '+5555555555'),
('Frank Thompson', 'frank@email.com', '+6666666666'),
('Grace Kim', 'grace@email.com', '+7777777777'),
('Henry Clark', 'henry@email.com', '+8888888888'),
('Ivy Chen', 'ivy@email.com', '+9999999999'),
('Jack Robinson', 'jack@email.com', '+1010101010'),
('Kate Adams', 'kate@email.com', '+1111111110'),
('Liam Murphy', 'liam@email.com', '+1212121212'),
('Maya Patel', 'maya@email.com', '+1313131313'),
('Noah Johnson', 'noah@email.com', '+1414141414'),
('Olivia Brown', 'olivia@email.com', '+1515151515');

-- Insert Tickets (registrations)
INSERT INTO tickets (event_id, attendee_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 4),
(3, 5), (3, 6),
(4, 7), (4, 8),
(5, 9), (5, 10),
(6, 11),
(7, 12),
(8, 13),
(9, 14),
(10, 15);