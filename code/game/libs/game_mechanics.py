def move_to_and_stop_at_point(ElementObject, positionB, time):
    BasicObject = ElementObject.basic
    positionA = BasicObject.position
    velocityA = BasicObject.velocity
    massA = BasicObject.mass
    velocityB = get_velocity_for_point_time(positionA, positionB, time)
    force = get_force_for_velocity(massA, velocityA, velocityB)
    ElementObject.create_impulse(force)


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

def get_force_for_velocity(objectMass, objectVelocity, desiredVelocity):
    return get_force_for_acceleration(objectMass,
        get_acceleration_for_velocity(objectVelocity,desiredVelocity))

def get_force_for_acceleration(objectMass, desiredAcceleration):
    return objectMass * desiredAcceleration

def get_acceleration_for_velocity(objectVelocity, desiredVelocity):
    return desiredVelocity - objectVelocity
