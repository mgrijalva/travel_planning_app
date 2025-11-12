from flask import render_template, redirect, request, url_for
from ..db import get_db
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


def trip_details(trip_id):
    conn = get_db()
    if request.method == "GET":
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("select * from trips where id = %s", (trip_id,))
            trip = cursor.fetchone()

            cursor.execute(
                "select * from events where trip_id = %s order by event_time",
                (trip_id,),
            )
            events = cursor.fetchall()
            return render_template(
                "trips/trip.html", events=events, trip=trip, trip_id=trip_id
            )
    else:
        event_name = request.form["event-name"]
        event_time = request.form["event-time"]
        address = request.form["address"]

        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                "insert into events (trip_id, event_name, event_time, address) values( %s, %s, %s, %s)",
                (trip_id, event_name, event_time, address),
            )
            conn.commit()
        return redirect(url_for("trip_details", trip_id=trip_id))
