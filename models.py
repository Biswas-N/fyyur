#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # Missing columns
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    # Relationships
    shows = db.relationship('Show', backref='venue', lazy=True, collection_class = list, cascade="save-update, delete")

    # String Abstraction
    def __repr__(self):
        return f'<Venue {self.id} - {self.name}>'

    # Utility methods
    def past_shows_count(self):
        count = 0
        presentDateTime = datetime.now()

        for show in self.shows:
            if show.start_time < presentDateTime:
                count += 1
        
        return count


    def upcoming_shows_count(self):
        count = 0
        presentDateTime = datetime.now()

        for show in self.shows:
            if show.start_time > presentDateTime:
                count += 1
        
        return count


    # JSON Abstraction
    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows_count": self.past_shows_count(),
            "upcoming_shows_count": self.upcoming_shows_count(),
        }


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # Missing columns
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    # Relationships
    shows = db.relationship('Show', backref='artist', lazy=True, collection_class = list, cascade="save-update, delete")

    # String Abstraction
    def __repr__(self):
        return f'<Artist {self.id} - {self.name}>'

    # Utility methods
    def past_shows_count(self):
        count = 0
        presentDateTime = datetime.now()

        for show in self.shows:
            if show.start_time < presentDateTime:
                count += 1
        
        return count


    def upcoming_shows_count(self):
        count = 0
        presentDateTime = datetime.now()

        for show in self.shows:
            if show.start_time > presentDateTime:
                count += 1
        
        return count

     # JSON Abstraction
    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows_count": self.past_shows_count(),
            "upcoming_shows_count": self.upcoming_shows_count(),
        }

class Show(db.Model):
    __tablename__= 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    # String Abstraction
    def __repr__(self):
        return f'<Show {self.id} - Artist {self.artist_id}, Venue {self.venue_id}>'