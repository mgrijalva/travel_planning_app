from . import db
from flask import Flask
from .controllers import trips_controller


def create_app() -> Flask:
    app = Flask(__name__)
    app.teardown_appcontext(db.release_conn)

    app.add_url_rule("/", view_func=trips_controller.list)
    app.add_url_rule("/trips", view_func=trips_controller.create_trip, methods=["POST"])
    app.add_url_rule(
        "/trips/<int:trip_id>",
        view_func=trips_controller.trip_details,
        methods=["GET", "POST"],
    )
    return app
