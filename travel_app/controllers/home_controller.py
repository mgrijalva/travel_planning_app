from flask import render_template
from ..db import get_db
from ..repositories.trip_repository import TripRepository

def index():
    # tr = TripRepository()

    conn = get_db()
    tr = TripRepository(conn)
    trips = tr.all()
    return render_template("home/index.html", trips=trips)