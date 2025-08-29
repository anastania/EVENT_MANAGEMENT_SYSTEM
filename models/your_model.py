from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Organizer(db.Model):
    __tablename__ = 'organizers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    events = db.relationship('Event', backref='organizer', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Organizer {self.name}>'

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizers.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='event', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.name}>'
    
    @property
    def attendee_count(self):
        return len(self.tickets)

class Attendee(db.Model):
    __tablename__ = 'attendees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='attendee', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Attendee {self.name}>'

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    attendee_id = db.Column(db.Integer, db.ForeignKey('attendees.id', ondelete='CASCADE'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate registrations
    __table_args__ = (db.UniqueConstraint('event_id', 'attendee_id', name='unique_event_attendee'),)
    
    def __repr__(self):
        return f'<Ticket Event:{self.event_id} Attendee:{self.attendee_id}>'