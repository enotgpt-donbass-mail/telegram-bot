import geopy.distance

def get_closest_location(target_latitude, target_longitude, locations):
    if not locations:
        return None

    closest_location = None
    min_distance = float('inf')

    target_point = (target_latitude, target_longitude)

    for location in locations:
        try:
            location_point = (location['coordinates'][0], location['coordinates'][1])
            distance = geopy.distance.geodesic(target_point, location_point).meters

            if distance < min_distance:
                min_distance = distance
                closest_location = location
        except (KeyError, TypeError):
            print(f"Warning: Invalid location format: {location}. Skipping.")
            continue

    return closest_location