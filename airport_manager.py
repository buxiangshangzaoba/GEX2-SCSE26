def find_flight(flights, flight_number):
    normalized = flight_number.upper()
    for key in flights:
        if key.upper() == normalized:
            return key
    return None


def passenger_exists(flights, flight_number, passenger_name):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return False
    
    target = passenger_name.strip().lower()
    for name in flights[flight_key]["passengers"]:
        if name.lower() == target:
            return True
    return False


def check_in_passenger(flights, flight_number, passenger_name, restricted_destinations):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    clean_name = passenger_name.strip()
    if clean_name == "":
        return "EMPTY_NAME"

    flight = flights[flight_key]

    if flight["destination"] in restricted_destinations:
        return "RESTRICTED"

    if passenger_exists(flights, flight_key, clean_name):
        return "DUPLICATE"

    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    flight["passengers"].append(clean_name)
    return "OK"


def remove_passenger(flights, flight_number, passenger_name):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    target = passenger_name.strip().lower()
    passenger_list = flights[flight_key]["passengers"]

    for name in passenger_list:
        if name.lower() == target:
            passenger_list.remove(name)
            return "OK"
            
    return "PASSENGER_NOT_FOUND"


def change_gate(flights, flight_number, new_gate, allowed_gates):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    if new_gate not in allowed_gates:
        return "INVALID_GATE"

    flights[flight_key]["gate"] = new_gate
    return "OK"


def flight_status(flights, flight_number):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return None

    flight = flights[flight_key]
    current = len(flight["passengers"])
    max_cap = flight["capacity"]

    if current >= max_cap:
        return "FULL"
    elif current >= max_cap - 1:
        return "ALMOST FULL"
    else:
        return "AVAILABLE"


def sorted_manifest(flights, flight_number):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return None

    return sorted(flights[flight_key]["passengers"])


def total_passengers(flights):
    total = 0
    for flight in flights.values():
        total = total + len(flight["passengers"])
    return total


def any_full_flight(flights):
    for flight in flights.values():
        if len(flight["passengers"]) >= flight["capacity"]:
            return True
    return False


def all_flights_have_passengers(flights):
    for flight in flights.values():
        if len(flight["passengers"]) == 0:
            return False
    return True


if __name__ == "__main__":
    flights = {
        "AY450": {
            "destination": "Helsinki",
            "departure": "08:30",
            "gate": "A2",
            "capacity": 5,
            "passengers": ["Alice Wong", "David Kim", "Fatima Ali"]
        },
        "SK27": {
            "destination": "Stockholm",
            "departure": "09:15",
            "gate": "B1",
            "capacity": 4,
            "passengers": ["Chen Wei", "George Smith"]
        }
    }

    allowed_gates = ("A1", "A2", "A3", "A4", "B1", "B2")
    restricted_destinations = {"Moscow", "Pyongyang"}

    print("Total passengers:", total_passengers(flights))
    print("Flight AY450 status:", flight_status(flights, "AY450"))
    print("Is Bob on AY450?", passenger_exists(flights, "AY450", "Bob"))
    print(check_in_passenger(flights, "AY450", "Bob", restricted_destinations))
    print("Is Bob on AY450 now?", passenger_exists(flights, "AY450", "Bob"))

