import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status

# ==============================================================================
# Branch Coverage Test Suite for ride_share_fare.py
# Targets 100% Branch Coverage across all decision points and conditions.
# ==============================================================================

# --- extra_distance_fare Tests ---

def test_extra_distance_fare_invalid_cab_type():
    # Branch 5->6 (cab_type not in INCLUDED_KM: True)
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("auto", 10, "city", False)

def test_extra_distance_fare_negative_distance():
    # Branch 5->7 (cab_type in INCLUDED_KM: False for branch 5->6)
    # Branch 7->8 (distance_km < 0: True)
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("sedan", -5, "city", False)

def test_extra_distance_fare_subscriber_non_suv():
    # Branch 10->11 (is_subscriber: True AND cab_type != 'suv': True) -> included becomes 5 + 3 = 8
    # Branch 13->14 (extra <= 0: True -> distance 8 - 8 = 0)
    assert extra_distance_fare("mini", 8, "city", True) == 0

def test_extra_distance_fare_non_subscriber():
    # Branch 10->12 (is_subscriber: False)
    # Branch 13->14 (extra <= 0: True -> distance 3 <= 5)
    assert extra_distance_fare("mini", 3, "city", False) == 0

def test_extra_distance_fare_subscriber_suv():
    # Branch 10->12 (is_subscriber: True BUT cab_type == 'suv') -> included stays 12
    # distance 10 <= 12 -> extra <= 0 -> 0
    assert extra_distance_fare("suv", 10, "city", True) == 0

def test_extra_distance_fare_city_short():
    # Branch 13->15 (extra > 0: True)
    # Branch 15->16 (zone == 'city': True -> rate = 12)
    # Branch 19->23 (extra > 20: False, extra = 10 -> 15 - 5)
    # Total = 10 * 12 = 120
    assert extra_distance_fare("mini", 15, "city", False) == 120

def test_extra_distance_fare_non_city_short():
    # Branch 15->18 (zone != 'city': True -> rate = 18)
    # Branch 19->23 (extra > 20: False, extra = 10 -> 18 - 8)
    # Total = 10 * 18 = 180
    assert extra_distance_fare("sedan", 18, "suburban", False) == 180

def test_extra_distance_fare_city_long():
    # Branch 19->20 (extra > 20: True)
    # Branch 21->23 (zone == 'outstation': False -> zone is 'city')
    # extra = 25 (distance 30, included 5), rate = 12 + 8 = 20 -> 25 * 20 = 500
    assert extra_distance_fare("mini", 30, "city", False) == 500

def test_extra_distance_fare_outstation_long():
    # Branch 19->20 (extra > 20: True)
    # Branch 21->22 (zone == 'outstation': True -> rate = 18 + 8 + 4 = 30)
    # extra = 25 (distance 33, included 8), rate = 30 -> 25 * 30 = 750
    assert extra_distance_fare("sedan", 33, "outstation", False) == 750


# --- seats_and_bags_ok Tests ---

def test_seats_and_bags_ok_wheelchair_passengers_le_2():
    # Branch 27->28 (needs_wheelchair: True)
    # passengers <= 2 -> True
    assert seats_and_bags_ok(2, 3, True) is True

def test_seats_and_bags_ok_wheelchair_passengers_gt_2():
    # Branch 27->28 (needs_wheelchair: True)
    # passengers > 2 -> False
    assert seats_and_bags_ok(3, 1, True) is False

def test_seats_and_bags_ok_no_wheelchair_passengers_gt_4():
    # Branch 27->29 (needs_wheelchair: False)
    # Branch 29->30 (passengers > 4: True -> False)
    assert seats_and_bags_ok(5, 1, False) is False

def test_seats_and_bags_ok_no_wheelchair_bags_le_2():
    # Branch 27->29 (needs_wheelchair: False)
    # Branch 29->31 (passengers <= 4: True)
    # bags <= 2 -> True
    assert seats_and_bags_ok(4, 2, False) is True

def test_seats_and_bags_ok_no_wheelchair_bags_gt_2():
    # Branch 27->29 (needs_wheelchair: False)
    # Branch 29->31 (passengers <= 4: True)
    # bags > 2 -> False
    assert seats_and_bags_ok(4, 3, False) is False


# --- pickup_status Tests ---

def test_pickup_status_scheduled_airport_on_time():
    # Branch 35->36 (is_scheduled: True -> cutoff = 10)
    # Branch 39->40 (is_airport: True -> cutoff = 20)
    # Branch 41->42 (minutes_early >= cutoff: True, e.g. 20 >= 20 -> 'on_time')
    assert pickup_status(20, True, True) == "on_time"

def test_pickup_status_scheduled_non_airport_delayed():
    # Branch 35->36 (is_scheduled: True -> cutoff = 10)
    # Branch 39->41 (is_airport: False -> cutoff = 10)
    # Branch 41->43 (minutes_early >= cutoff: False)
    # Branch 43->44 (minutes_early >= cutoff - 15: True, e.g. cutoff-15 = -5, minutes_early = 0 -> 'delayed')
    assert pickup_status(0, True, False) == "delayed"

def test_pickup_status_scheduled_non_airport_missed():
    # Branch 35->36 (is_scheduled: True -> cutoff = 10)
    # Branch 39->41 (is_airport: False -> cutoff = 10)
    # Branch 41->43 (minutes_early >= 10: False)
    # Branch 43->45 (minutes_early >= -5: False, e.g. -6 -> 'missed')
    assert pickup_status(-6, True, False) == "missed"

def test_pickup_status_unscheduled_airport_on_time():
    # Branch 35->38 (is_scheduled: False -> cutoff = 5)
    # Branch 39->40 (is_airport: True -> cutoff = 15)
    # Branch 41->42 (minutes_early >= 15: True -> 'on_time')
    assert pickup_status(15, False, True) == "on_time"

def test_pickup_status_unscheduled_non_airport_delayed():
    # Branch 35->38 (is_scheduled: False -> cutoff = 5)
    # Branch 39->41 (is_airport: False -> cutoff = 5)
    # Branch 41->43 (minutes_early >= 5: False)
    # Branch 43->44 (minutes_early >= -10: True, e.g. -5 -> 'delayed')
    assert pickup_status(-5, False, False) == "delayed"

def test_pickup_status_unscheduled_non_airport_missed():
    # Branch 35->38 (is_scheduled: False -> cutoff = 5)
    # Branch 39->41 (is_airport: False -> cutoff = 5)
    # Branch 41->43 (minutes_early >= 5: False)
    # Branch 43->45 (minutes_early >= -10: False, e.g. -11 -> 'missed')
    assert pickup_status(-11, False, False) == "missed"
