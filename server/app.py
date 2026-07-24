from flask import Flask, jsonify
from models import db, Event, Session, Speaker

app = Flask(__name__)

# Basic configuration – tests usually override SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/events", methods=["GET"])
def get_events():
    events = db.session.query(Event).all()

    return jsonify([
        {
            "id": event.id,
            "name": event.name,
            "location": event.location,
        }
        for event in events
    ]), 200


@app.route("/events/<int:id>/sessions", methods=["GET"])
def get_event_sessions(id):
    event = db.session.get(Event, id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    return jsonify([
        {
            "id": session.id,
            "title": session.title,
            "start_time": (
                session.start_time.isoformat()
                if session.start_time
                else None
            ),
        }
        for session in event.sessions
    ]), 200


@app.route("/speakers", methods=["GET"])
def get_speakers():
    speakers = db.session.query(Speaker).all()

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name,
        }
        for speaker in speakers
    ]), 200


@app.route("/speakers/<int:id>", methods=["GET"])
def get_speaker_by_id(id):
    speaker = db.session.get(Speaker, id)

    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404

    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": (
            speaker.bio.bio_text
            if speaker.bio
            else "No bio available"
        ),
    }), 200


@app.route("/sessions/<int:id>/speakers", methods=["GET"])
def get_session_speakers(id):
    session = db.session.get(Session, id)

    if session is None:
        return jsonify({"error": "Session not found"}), 404

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": (
                speaker.bio.bio_text
                if speaker.bio
                else "No bio available"
            ),
        }
        for speaker in session.speakers
    ]), 200


if __name__ == "__main__":
    app.run(debug=True)
