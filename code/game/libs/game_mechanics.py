def move_to_and_stop_at_point(ElementObject, position, speed = 0.1):
    positionA = ElementObject.get_position()


def get_velocity_for_point_time(positionA, positionB, time):
    """
    Returns the average velocity required for an object at point A to be moving
    to reach point B in the time given.

    :param positionA: Current position (x,y)
    :param positionB: Destination position (x,y)
    :param time: Time in seconds from now that the destination should be reached.
    :return: vector
    """
    difference_vector = positionA - positionB
    return ( difference_vector / time )