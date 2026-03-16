import random

buses = [
    {"bus_id": "BUS001", "lat": 39.990, "lng": 116.290},
    {"bus_id": "BUS002", "lat": 39.985, "lng": 116.300}
]

def get_bus_positions():

    for bus in buses:
        bus["lat"] += random.uniform(-0.0005, 0.0005)
        bus["lng"] += random.uniform(-0.0005, 0.0005)

    return buses