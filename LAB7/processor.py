import math

def parse_trip(text):
    """
    Parses trip string in format 'cab:distance' (e.g., 'sedan:12').
    Returns tuple (Cab_Name_Title_Case, distance_float) or None if invalid.
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    cab, km = parts
    cab = cab.strip()
    if not cab:
        return None
    try:
        km_val = float(km.strip())
        if not math.isfinite(km_val) or km_val < 0:
            return None
        return cab.title(), km_val
    except (ValueError, TypeError):
        return None

def fare_average(fares_csv):
    """
    Calculates integer average of comma-separated fare values (e.g., '120,95,210').
    Returns average or 0 if invalid/empty.
    """
    if not isinstance(fares_csv, str):
        return 0
    parts = [r.strip() for r in fares_csv.split(',') if r.strip()]
    if not parts:
        return 0
    try:
        values = [int(r) for r in parts]
        if not values:
            return 0
        return sum(values) // len(values)
    except (ValueError, TypeError):
        return 0

def payable_fare(text):
    """
    Calculates payable fare given 'fare|promo' (e.g., '250|30') including 18% tax minus promo.
    Returns payable fare or 0.0 if invalid.
    """
    if not isinstance(text, str):
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    fare_str, promo_str = parts
    try:
        fare = float(fare_str.strip())
        promo = float(promo_str.strip())
        if not (math.isfinite(fare) and math.isfinite(promo)):
            return 0.0
        if fare < 0 or promo < 0:
            return 0.0
        total = fare * 1.18 - promo
        return max(total, 0.0)
    except (ValueError, TypeError):
        return 0.0

def main():
    print("==== Running parse_trip ====")
    user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
    result = parse_trip(user_input)
    print("Cab and Distance:", result)

    print("\n==== Running fare_average ====")
    user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
    result = fare_average(user_input)
    print("Average Fare:", result)

    print("\n==== Running payable_fare ====")
    user_input = input("Enter fare|promo (e.g. 250|30): ")
    result = payable_fare(user_input)
    print("Payable Fare:", result)

if __name__ == "__main__":
    main()
