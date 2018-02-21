import numpy as np


class Rectangle(object):
    def __init__(self, x, y, dx, dy, length, width, agent_id):

        self._agent_id = agent_id
        self._theta = np.arctan2(dx, dy)
        self.vertexes = np.array(\
                [[- width/2, width/2, width/2, - width/2],
                [- length/2,- length/2, length/2,  length/2]])

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
