import numpy as np
from math import pi


def SAT(rectA, rectB):
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
    def __init__(self, x, y, dx, dy, length, width, agent_id):

        self._agent_id = agent_id
        self._center = np.array([x, y])
        self._theta = np.arctan2(dx, dy)
        self._radius = np.linalg.norm([length, width]) / 2
        self.vertexes = np.array(\
                [[- width/2, width/2, width/2, - width/2],
                [- length/2,- length/2, length/2,  length/2]])
        self.vertexes = Rectangle.rotate(self.vertexes, self._theta)
        self.vertexes = Rectangle.translate(self.vertexes, x, y)

    # Method defined for using the sort function
    def __lt__(self, other):
        if self._center[0] != other.center[0]:
            return self._center[0] < other._center[0]
        else:
            return self._center[1] < other._center[1]

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
