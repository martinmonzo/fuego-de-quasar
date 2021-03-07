def is_there_any_unknown_distance(satellites_info):
    """
    Determine whether there are satellites whose distance 
    to the transmitter has not been discovered yet.

    Args:
        - satellites_info (QuerySet): all the information already known about the satellites.

    Returns:
        bool:
            - True if there is at least one satellite whose distance has not been discovered.
            - False otherwise.
    """
    return satellites_info.filter(distance_from_transmitter__isnull=True).count() > 0


def get_distances(satellites_info):
    """
    Retrieve the distance from the transmitter to each satellite.

    Args:
        - satellites_info (QuerySet): all the information already known about the satellites.

    Returns:
        dict[str, float]: the distance from the transmitter to each satellite.
    """
    return {
        satellite.name: satellite.distance_from_transmitter
        for satellite in satellites_info
    }


def get_distance_by_satellite(satellites, satellite_name):
    """
    Retrieve the distance from the transmitter to a specific satellite, given its
    distances to every satellite, filtering by the desired satellite name.

    Args:
        - satellites (list[dict]): information about each satellite.
        - satellite_name (str): name of the satellite to filter by.
    
    Returns:
        A float that represents the distance from the transmitter to the desired satellite.
    """
    satellite = next((sat for sat in satellites if sat['name'] == satellite_name), {})
    return satellite['distance']
