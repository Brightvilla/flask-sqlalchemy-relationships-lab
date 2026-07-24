from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Global metadata with naming convention for foreign keys
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# Association table for the Session <-> Speaker many-to-many relationship
session_speakers = db.Table(
    "session_speakers",
    db.metadata,
    db.Column(
        "session_id",
        db.Integer,
        db.ForeignKey("sessions.id"),
        primary_key=True,
    ),
    db.Column(
        "speaker_id",
        db.Integer,
        db.ForeignKey("speakers.id"),
        primary_key=True,
    ),
)


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # One-to-many: Event -> Session
    sessions = db.relationship(
        "Session",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Event {self.id}: {self.name}>"


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=True,
    )

    # Many-to-one: Session -> Event
    event = db.relationship(
        "Event",
        back_populates="sessions",
    )

    # Many-to-many: Session <-> Speaker
    speakers = db.relationship(
        "Speaker",
        secondary=session_speakers,
        back_populates="sessions",
    )

    def __repr__(self) -> str:
        return f"<Session {self.id}: {self.title}>"


class Speaker(db.Model):
    __tablename__ = "speakers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # One-to-one: Speaker -> Bio
    bio = db.relationship(
        "Bio",
        back_populates="speaker",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Many-to-many: Speaker <-> Session
    sessions = db.relationship(
        "Session",
        secondary=session_speakers,
        back_populates="speakers",
    )

    def __repr__(self) -> str:
        return f"<Speaker {self.id}: {self.name}>"


class Bio(db.Model):
    __tablename__ = "bios"

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.String, nullable=False)

    speaker_id = db.Column(
        db.Integer,
        db.ForeignKey("speakers.id"),
        unique=True,
        nullable=False,
    )

    # One-to-one: Bio -> Speaker
    speaker = db.relationship(
        "Speaker",
        back_populates="bio",
    )

    def __repr__(self) -> str:
        return f"<Bio {self.id}>"