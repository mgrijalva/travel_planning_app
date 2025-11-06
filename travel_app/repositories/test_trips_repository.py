from travel_app.repositories.trips_repository import dummy_function


def test_dummy_function():
    assert dummy_function(1, 1) == 2
    assert dummy_function(-1, 1) == 0
