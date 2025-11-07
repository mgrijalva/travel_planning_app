from flask import render_template, redirect, request
from ..db import get_db
from ..repositories.trips_repository import TripsRepository
from psycopg2.extras import DictCursor


def list():
    conn = get_db()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(
            """
            select * from trips;
        """
        )
        data = cursor.fetchall()
    return render_template("trips/index.html", trips=data)


def create_trip():
    title = request.form["title"]
    start_date = request.form["start-date"]
    end_date = request.form["end-date"]

    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            """
            insert into trips (title,start_date,end_date) values(%s, %s, %s)
                       """,
            (title, start_date, end_date),
        )
        conn.commit()
    return redirect("/")
