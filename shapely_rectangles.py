import numpy as np
from math import pi
from shapely.geometry import Polygon


def check_collisions(rectangles):
    """
    Takes a list of rectangle objects and returns tuples of ids
    of colliding rectangles.
    """
    rectangles.sort()
    rect_radius = [rect._radius for rect in rectangles]
    max_radius = np.max(rect_radius)
    overlaps = []
    for i, rect in enumerate(rectangles):
        r1 = rect_radius[i]
        for j, other_rect in enumerate(rectangles[i + 1:]):
            r2 = rect_radius[j + i + 1]
            diff = other_rect.center - rect.center
            if diff[0] - r1 <= max_radius:
                if np.linalg.norm(diff) <= r1 + r2:
                    if SAT(rect, other_rect):
                        overlaps.append((rect.id, other_rect.id))
            else:
                break
    return overlaps


def check_overlap(rect, other_rect):
    return rect.poly.overlaps(other_rect.poly) or rect.poly.intersects(
        other_rect.poly)


def SAT(rectA, rectB):
    ''' 
    Seperating Axis Theorem
    '''
    axes = rectA.get_axes()
    axes += rectB.get_axes()

    for axis in axes:
        projection_a = rectA.project(axis)
        projection_b = rectB.project(axis)
        overlapping = overlap(projection_a, projection_b)
        if not overlapping:
            return False
    return True


# orthogonal of vector (x,y) is (y,-x)
def orthogonal(v):
    return (v[1], -v[0])


def contains(n, range_):
    a = range_[0]
    b = range_[1]
    if b < a:
        a = range_[1]
        b = range_[0]
    return (n >= a) and (n <= b)


def overlap(a, b):
    if contains(a[0], b) or contains(a[1], b) or \
        contains(b[0], a) or contains(b[1], a):
        return True
    return False


class Rectangle(object):
    def __init__(self, x, y, dx, dy, width, length, agent_id):

        self.id = agent_id
        self.center = np.array([x, y])
        self._theta = np.arctan2(dx, dy)
        self._radius = np.linalg.norm([length, width]) / 2
        self.vertexes = np.array(\
                [[- width/2, width/2, width/2, - width/2],
                [- length/2,- length/2, length/2,  length/2]])
        self.vertexes = Rectangle.rotate(self.vertexes, self._theta)
        self.vertexes = Rectangle.translate(self.vertexes, x, y)

        self.poly = Polygon(self.vertexes.T)

    # Method defined for using the sort function
    def __lt__(self, other):
        if self.center[0] != other.center[0]:
            return self.center[0] < other.center[0]
        else:
            return self.center[1] < other.center[1]

    # T = R
    @classmethod
    def rotate(cls, matrix, theta):
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta),
                                     np.cos(theta)]])
        return np.matmul(rotation_matrix, matrix)

    # T = M
    @classmethod
    def translate(cls, matrix, dx, dy):
        matrix = np.append(matrix, [[1, 1, 1, 1]], axis=0)
        translation_matrix = np.array([[1, 0, dx], [0, 1, dy]])
        matrix = np.matmul(translation_matrix, matrix)
        return matrix[:, :4]

    # index = 0 is first edge,1 second-edge
    def edge_direction(self, index):
        return (self.vertexes[:,index%len(self.vertexes[0,:])] - \
         self.vertexes[:,(index+1) % len(self.vertexes[0,:])])

    def vertices_to_edges(self):
        self.edges = [self.edge_direction(i) \
        for i in range(len(self.vertexes[0,:]))]

    def get_axes(self):
        self.vertices_to_edges()
        return [orthogonal(edge) for edge in self.edges]

    # No need to normalize
    def project(self, axis):
        dots = [np.dot(axis, self.vertexes)]
        return [np.min(dots), np.max(dots)]
