from flask_sqlalchemy import SQLAlchemy

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
    genres = db.Column(db.String)
    shows = db.relationship('Show', backref='venue', lazy=True, cascade="all, delete")
    isLookingForTalent = db.Column(db.Boolean, default=False)
    seekingDescription = db.Column(db.String)
    website_link = db.Column(db.String(150))


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(150))
    shows = db.relationship('Show', backref='artist', lazy=True, cascade="all, delete")
    isLookingForVenues = db.Column(db.Boolean, default=False)
    seekingDescription = db.Column(db.String)


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venueId = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artistId = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    showTime = db.Column(db.DateTime)
