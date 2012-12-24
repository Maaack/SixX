def move_to_point_and_stop(GameObject, ElementObject, positionB, time, threshold = 5.0):
    # TODO Take into account the maximum rate of impulse for an object for calculating desired velocity
    BasicObject = ElementObject.BasicObject
    if BasicObject == None:
        return True
    remaining_time = time - GameObject.game_time
    positionA = BasicObject.position
    velocityA = BasicObject.velocity
    massA = BasicObject.mass
    distance = positionA.get_distance(positionB)
    # TODO Take into account time to decelerate if there is a maximum rate of impulse
    if distance < threshold:
        if velocityA != (0,0):
            velocityB = (0,0)
        else:
            return True
    else:
        velocityB = get_velocity_for_point_time(positionA, positionB, remaining_time)
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
    if time < 0 :
        time = 0.1
    difference_vector =  positionB - positionA
    return ( difference_vector / time )

def get_force_for_velocity(objectMass, objectVelocity, desiredVelocity):
    # print "objectMass: "+str(objectMass)+"; objectVelocity: "+str(objectVelocity)+"; desiredVelocity: "+str(desiredVelocity)
    return get_force_for_acceleration(objectMass,
        get_acceleration_for_velocity(objectVelocity,desiredVelocity))

def get_force_for_acceleration(objectMass, desiredAcceleration):
    return objectMass * desiredAcceleration

def get_acceleration_for_velocity(objectVelocity, desiredVelocity):
    return desiredVelocity - objectVelocity
