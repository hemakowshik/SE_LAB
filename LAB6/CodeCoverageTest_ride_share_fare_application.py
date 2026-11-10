import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status

# Test cases designed for Code Coverage (Line Coverage >= 90%, achieves 100% line coverage)

def test_extra_distance_fare_invalid_cab_type():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("truck", 10, "city", False)

def test_extra_distance_fare_invalid_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)

def test_extra_distance_fare_zero_extra_with_subscriber():
    # mini: included = 5 + 3 = 8 km, distance = 7 km -> extra = -1 <= 0 -> returns 0
    assert extra_distance_fare("mini", 7, "city", True) == 0

def test_extra_distance_fare_city_short():
    # mini: included = 5, distance = 10, extra = 5 <= 20, zone = "city" -> rate = 12 -> 5 * 12 = 60
    assert extra_distance_fare("mini", 10, "city", False) == 60

def test_extra_distance_fare_non_city_short():
    # sedan: included = 8, distance = 18, extra = 10 <= 20, zone = "rural" -> rate = 18 -> 10 * 18 = 180
    assert extra_distance_fare("sedan", 18, "rural", False) == 180

def test_extra_distance_fare_outstation_long():
    # suv: included = 12 (subscriber doesn't add for suv), distance = 42, extra = 30 > 20
    # zone = "outstation" -> rate = 18 + 8 + 4 = 30 -> 30 * 30 = 900
    assert extra_distance_fare("suv", 42, "outstation", True) == 900

def test_seats_and_bags_ok_wheelchair_ok():
    assert seats_and_bags_ok(2, 4, True) is True

def test_seats_and_bags_ok_wheelchair_too_many():
    assert seats_and_bags_ok(3, 1, True) is False

def test_seats_and_bags_ok_passengers_too_many():
    assert seats_and_bags_ok(5, 1, False) is False

def test_seats_and_bags_ok_bags_ok():
    assert seats_and_bags_ok(4, 2, False) is True

def test_seats_and_bags_ok_too_many_bags():
    assert seats_and_bags_ok(4, 3, False) is False

def test_pickup_status_scheduled_airport_on_time():
    # is_scheduled=True (cutoff=10), is_airport=True (cutoff=20), minutes_early=25 >= 20 -> on_time
    assert pickup_status(25, True, True) == "on_time"

def test_pickup_status_unscheduled_delayed():
    # is_scheduled=False (cutoff=5), is_airport=False (cutoff=5), cutoff-15 = -10, minutes_early=0 -> delayed
    assert pickup_status(0, False, False) == "delayed"

def test_pickup_status_missed():
    # is_scheduled=False (cutoff=5), is_airport=False (cutoff=5), cutoff-15 = -10, minutes_early=-15 -> missed
    assert pickup_status(-15, False, False) == "missed"
