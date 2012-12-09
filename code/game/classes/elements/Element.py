from game.libs import make_hash

class Element(object):

    _Game = None
    BasicObject = None

    def __init__(self):
        self._id = make_hash()

    def get_id(self):
        return self._id

    id = property(get_id)

    def get_physical_object(self):
        return self.BasicObject.body

    def get_movable_object(self):
        return self.BasicObject.body

    def get_angle(self):
        return self.BasicObject.body.angle

    def get_position(self):
        return self.BasicObject.body.position

    def get_points(self):
        return self.BasicObject.get_points()

    def is_hovering(self, position):
        return self.BasicObject.shape.point_query(position)

    def is_selected(self, position):
        return self.BasicObject.shape.point_query(position)

    def is_deselected(self, position):
        return self.BasicObject.shape.point_query(position)

    def destroy(self):
        self.destroy_Basics()
        self._Game.drop_Object(self)

    def destroy_Basics(self):
        self.destroy_Basic()

    def destroy_Basic(self):
        if hasattr(self.BasicObject, 'destroy'):
            self.BasicObject.destroy()
        self.BasicObject = None