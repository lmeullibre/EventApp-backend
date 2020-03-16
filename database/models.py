from database import db
from sqlalchemy import ForeignKey
from sqlalchemy_utils.types.password import PasswordType
import datetime


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
                )


backers = db.Table('backers',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
                   db.Column('backed_amount', db.Float())
                   )


watchers = db.Table('watchers',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
                    )


class VotedTest(db.Model):
    __tablename__ = "votedtest"
    event_id = db.Column(db.Integer, ForeignKey('event.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    stars = db.Column(db.Integer())
    votes = db.relationship("Event", back_populates="votes")
    voted = db.relationship("User", back_populates="voted")


class Funded(db.Model):
    __tablename__ = "funded"
    event_id = db.Column(db.Integer, ForeignKey('event.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    fund_amount = db.Column(db.Float())
    backers = db.relationship("Event", back_populates="backers")
    backed = db.relationship("User", back_populates="backed")


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000))
    photo = db.Column(db.String(2000))
    funding_start_date = db.Column(db.DateTime(), nullable=False)
    funding_end_date = db.Column(db.DateTime(), nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False)
    goal = db.Column(db.Float)
    long = db.Column(db.Numeric(11, 8))
    lat = db.Column(db.Numeric(11, 8))
    stars = db.Column(db.Float)
    event_start_date = db.Column(db.DateTime(), nullable=False)
    event_end_date = db.Column(db.DateTime())
    location = db.Column(db.String(200), nullable=False)
    user_creator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('tags', lazy=True))
    watchers = db.relationship("User", secondary=watchers, backref="watching")
    backers = db.relationship("Funded", back_populates="backers")
    votes = db.relationship("VotedTest", back_populates="votes")

    def __init__(self, name, description, funding_start_date, funding_end_date, goal, event_start_date, event_end_date, location, user_creator, lat, long, photo):
        self.name = name
        self.description = description
        self.funding_start_date = funding_start_date
        self.funding_end_date = funding_end_date
        self.creation_date = datetime.datetime.now()
        self.goal = goal
        self.event_start_date = event_start_date
        self.event_end_date = event_end_date
        self.location = location
        self.user_creator = user_creator
        self.lat = lat
        self.long = long
        self.photo = photo

    def __repr__(self):
        return '<Event %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(500))
    birth_date = db.Column(db.Date)
    password = db.Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt']
    ), nullable=False)
    bio = db.Column(db.String(2000))
    telephone = db.Column(db.String(20))
    instagram = db.Column(db.String(100))
    backed = db.relationship("Funded", back_populates="backed")
    voted = db.relationship("VotedTest", back_populates="voted")

    def __init__(self, name, mail, photo, birth_date, password, bio, telephone, instagram):
        self.name = name
        self.mail = mail
        self.photo = photo
        self.birth_date = birth_date
        self.password = password
        self.bio = bio
        self.telephone = telephone
        self.instagram = instagram

    def __repr__(self):
        return '<User %r>' % self.name


# Comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    text = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)

    def __init__(self, user_id, event_id, text):
        self.user_id = user_id
        self.event_id = event_id
        self.text = text
        self.timestamp = datetime.datetime.today()

    def __repr__(self):
        return '<Comment %r>' % self.text


class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    refresh_token = db.Column(db.String(500), unique=True)
    user_agent_hash = db.Column(db.String(80))


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, ForeignKey('event.id'), nullable=False)
    content = db.Column(db.Text)

    def __init__(self, user_id, event_id, content):
        self.user_id = user_id
        self.event_id = event_id
        self.content = content


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100))

    def __init__(self, tag):
        self.tag_name = tag
