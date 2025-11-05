from . import db
from flask import Flask, g
from .controllers import home_controller

def create_app() -> Flask:
    app = Flask(__name__)
    app.teardown_appcontext(db.release_conn)

    app.add_url_rule("/", view_func=home_controller.index)

    return app