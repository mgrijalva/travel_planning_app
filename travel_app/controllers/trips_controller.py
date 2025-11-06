from flask import render_template
from ..db import get_db
from ..repositories.trips_repository import TripsRepository


def list():
    conn = get_db()
    tr = TripsRepository(conn)
    trips = tr.all()
    return render_template("trips/index.html", trips=trips)
