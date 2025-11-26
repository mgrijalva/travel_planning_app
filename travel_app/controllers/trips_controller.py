from flask import render_template, redirect, request, url_for
from ..db import get_db
from psycopg2.extras import DictCursor
import os
import requests
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
        current_address = request.form["address"]

        # create the event in the database, along with the travel time
        conn = get_db()
        with conn.cursor() as cursor:
            # find the previous event (if any) in that day
            cursor.execute(
                "select id,address from events where event_time < %s and trip_id = %s  order by event_time desc limit 1",
                (event_time, trip_id),
            )
            previous_address_tup = cursor.fetchone()
            if previous_address_tup is not None:
                prev_id = previous_address_tup[0]
                prev_address = previous_address_tup[1]
                calculated_travel_time = get_travel_time(prev_address, current_address)
                cursor.execute(
                    "update events set travel_time_to_next_event = %s where id=%s",
                    (calculated_travel_time, prev_id),
                )
            ## do the same for the one after if any
            cursor.execute(
                "select id,address from events where event_time > %s and trip_id = %s  order by event_time asc limit 1",
                (event_time, trip_id),
            )
            post_address_tup = cursor.fetchone()
            if post_address_tup is not None:
                post_id = post_address_tup[0]
                post_address = post_address_tup[1]
                calculated_post_travel_time = get_travel_time(
                    post_address, current_address
                )
                cursor.execute(
                    "update events set travel_time_to_next_event = %s where id=%s",
                    (calculated_post_travel_time, post_id),
                )
            # import pdb

            # pdb.set_trace()

            # find the travel time between the two events
            ## need to calculate if it has a before event prev && next
            # need to display travel time??
            # save the travel time?
            cursor.execute(
                "insert into events (trip_id, event_name, event_time, address) values( %s, %s, %s, %s)",
                (trip_id, event_name, event_time, current_address),
            )
            conn.commit()
        return redirect(url_for("trip_details", trip_id=trip_id))
