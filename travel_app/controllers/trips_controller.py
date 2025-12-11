from flask import render_template, redirect, request, url_for
from ..db import get_db
from psycopg2.extras import DictCursor
import os
from datetime import datetime
from travel_app.service.trip_estimator_service import get_travel_time

api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")


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
        mode_transportation = request.form["mode-transportation"]

        dt = datetime.fromisoformat(event_time)
        event_date = dt.date()

        conn = get_db()
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "insert into events (trip_id, event_name, event_time, address, mode_of_transportation) "
                "values (%s, %s, %s, %s, %s)",
                (trip_id, event_name, event_time, address, mode_transportation),
            )
            conn.commit()
            cursor.execute(
                """
                SELECT id, address, mode_of_transportation
                FROM events
                WHERE trip_id = %s
                AND DATE(event_time) = %s
                ORDER BY event_time
                """,
                (trip_id, event_date),
            )
            events = cursor.fetchall()

            # Recalculate time travel btwn consecutive events
            for i in range(len(events) - 1):
                from_addr = events[i]["address"]
                to_addr = events[i + 1]["address"]

                mode_of_transportation = events[i + 1].get("mode_of_transportation")

                travel_time = get_travel_time(
                    from_addr, to_addr, mode_of_transportation
                )

                cursor.execute(
                    "UPDATE events SET travel_time_to_next_event = %s WHERE id = %s",
                    (travel_time, events[i]["id"]),
                )

            # no travel time needed for last event of day
            cursor.execute(
                "UPDATE events SET travel_time_to_next_event = NULL WHERE id = %s",
                (events[-1]["id"],),
            )

            conn.commit()
            return redirect(url_for("trip_details", trip_id=trip_id))
