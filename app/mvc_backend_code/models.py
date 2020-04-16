#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from sqlalchemy.dialects.postgresql import JSON
from app import db


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#Association Table
#Links to both Venue and Artist (One to Many Relationship with both tables)
class Shows(db.Model):
  
  shows = db.Table("shows",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("Artist.id")), #Foreign key
    db.Column("venue_id", db.Integer, db.ForeignKey("Venue.id")), #Foreign key
    db.Column("start_time", db.DateTime))

#Venue table
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(JSON)  #Used JSON to process genres as a list of strings
    facebook_link = db.Column(db.String(120))

    website_link = db.Column(db.String(120))
    image_link = db.Column(db.String())
    seeking_talent = db.Column(db.String())
    seeking_description = db.Column(db.String())

    show = db.relationship('Shows', backref=db.backref("Venue", lazy=True))

    def __repr__(self):
        return f'<Venue {self.name}>'


#Artist table
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(JSON)  #Used JSON to process genres as a list of strings
    facebook_link = db.Column(db.String(120))

    website_link = db.Column(db.String(120))
    image_link = db.Column(db.String())
    seeking_venues = db.Column(db.String())
    seeking_description = db.Column(db.String())

    show = db.relationship('Shows', backref=db.backref("Artist", lazy=True))

    def __repr__(self):
        return f'<Artist: {self.name}>'

    