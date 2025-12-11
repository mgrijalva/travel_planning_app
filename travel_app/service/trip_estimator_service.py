import googlemaps
from datetime import datetime
import os


def get_travel_time(
    previous_address: str, current_address: str, mode_transportation: str
) -> int:
    gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])
    now = datetime.now()
    directions_result = gmaps.directions(  # type: ignore
        previous_address, current_address, mode=mode_transportation, departure_time=now
    )
    duration_of_addresses: int = directions_result[0]["legs"][0]["duration"]["value"]

    return duration_of_addresses
