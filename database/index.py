from models.your_model import db, Event, Organizer, Attendee, Ticket
from datetime import datetime, date

def init_db(app):
    """Initialize database with the Flask app"""
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if Organizer.query.count() == 0:
            seed_data()

def seed_data():
    """Seed database with initial data"""
    try:
        # Create Organizers
        organizers = [
            Organizer(name='John Smith', email='john@email.com', phone='+1234567890'),
            Organizer(name='Sarah Johnson', email='sarah@email.com', phone='+1234567891'),
            Organizer(name='Mike Wilson', email='mike@email.com', phone='+1234567892'),
            Organizer(name='Emily Brown', email='emily@email.com', phone='+1234567893'),
            Organizer(name='David Davis', email='david@email.com', phone='+1234567894'),
            Organizer(name='Lisa Garcia', email='lisa@email.com', phone='+1234567895'),
            Organizer(name='Tom Martinez', email='tom@email.com', phone='+1234567896'),
            Organizer(name='Anna Taylor', email='anna@email.com', phone='+1234567897'),
            Organizer(name='Chris Anderson', email='chris@email.com', phone='+1234567898'),
            Organizer(name='Maria Rodriguez', email='maria@email.com', phone='+1234567899'),
        ]
        
        for organizer in organizers:
            db.session.add(organizer)
        
        db.session.commit()
        
        # Create Events
        events = [
            Event(name='Tech Conference 2024', date=date(2024, 12, 15), location='San Francisco, CA', 
                  description='Annual technology conference featuring the latest innovations', organizer_id=1),
            Event(name='Music Festival', date=date(2024, 11, 20), location='Austin, TX', 
                  description='Three-day music festival with top artists', organizer_id=2),
            Event(name='Business Summit', date=date(2024, 12, 5), location='New York, NY', 
                  description='Networking event for business professionals', organizer_id=3),
            Event(name='Art Exhibition', date=date(2024, 11, 30), location='Los Angeles, CA', 
                  description='Contemporary art exhibition by emerging artists', organizer_id=4),
            Event(name='Food & Wine Festival', date=date(2024, 12, 10), location='Portland, OR', 
                  description='Celebration of local cuisine and wines', organizer_id=5),
            Event(name='Marathon 2024', date=date(2024, 11, 25), location='Chicago, IL', 
                  description='Annual city marathon for all skill levels', organizer_id=6),
            Event(name='Book Fair', date=date(2024, 12, 1), location='Seattle, WA', 
                  description='Independent authors and publishers showcase', organizer_id=7),
            Event(name='Gaming Convention', date=date(2024, 11, 28), location='Las Vegas, NV', 
                  description='Gaming enthusiasts convention with competitions', organizer_id=8),
            Event(name='Science Fair', date=date(2024, 12, 8), location='Boston, MA', 
                  description='Student science projects and demonstrations', organizer_id=9),
            Event(name='Fashion Week', date=date(2024, 12, 12), location='Miami, FL', 
                  description='Latest fashion trends and designer showcases', organizer_id=10),
        ]
        
        for event in events:
            db.session.add(event)
        
        db.session.commit()
        
        # Create Attendees
        attendees = [
            Attendee(name='Alice Cooper', email='alice@email.com', phone='+1111111111'),
            Attendee(name='Bob Miller', email='bob@email.com', phone='+2222222222'),
            Attendee(name='Carol White', email='carol@email.com', phone='+3333333333'),
            Attendee(name='Daniel Lee', email='daniel@email.com', phone='+4444444444'),
            Attendee(name='Emma Wilson', email='emma@email.com', phone='+5555555555'),
            Attendee(name='Frank Thompson', email='frank@email.com', phone='+6666666666'),
            Attendee(name='Grace Kim', email='grace@email.com', phone='+7777777777'),
            Attendee(name='Henry Clark', email='henry@email.com', phone='+8888888888'),
            Attendee(name='Ivy Chen', email='ivy@email.com', phone='+9999999999'),
            Attendee(name='Jack Robinson', email='jack@email.com', phone='+1010101010'),
            Attendee(name='Kate Adams', email='kate@email.com', phone='+1111111110'),
            Attendee(name='Liam Murphy', email='liam@email.com', phone='+1212121212'),
            Attendee(name='Maya Patel', email='maya@email.com', phone='+1313131313'),
            Attendee(name='Noah Johnson', email='noah@email.com', phone='+1414141414'),
            Attendee(name='Olivia Brown', email='olivia@email.com', phone='+1515151515'),
        ]
        
        for attendee in attendees:
            db.session.add(attendee)
        
        db.session.commit()
        
        # Create some ticket registrations
        tickets = [
            Ticket(event_id=1, attendee_id=1),
            Ticket(event_id=1, attendee_id=2),
            Ticket(event_id=1, attendee_id=3),
            Ticket(event_id=2, attendee_id=1),
            Ticket(event_id=2, attendee_id=4),
            Ticket(event_id=3, attendee_id=5),
            Ticket(event_id=3, attendee_id=6),
            Ticket(event_id=4, attendee_id=7),
            Ticket(event_id=4, attendee_id=8),
            Ticket(event_id=5, attendee_id=9),
            Ticket(event_id=5, attendee_id=10),
            Ticket(event_id=6, attendee_id=11),
            Ticket(event_id=7, attendee_id=12),
            Ticket(event_id=8, attendee_id=13),
            Ticket(event_id=9, attendee_id=14),
            Ticket(event_id=10, attendee_id=15),
        ]
        
        for ticket in tickets:
            db.session.add(ticket)
        
        db.session.commit()
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.session.rollback()