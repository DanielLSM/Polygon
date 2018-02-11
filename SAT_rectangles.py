import numpy as np
import matplotlib.pyplot as plt
from math import pi

def SAT(rectA,rectB):

    axes = rectA.get_axes()
    axes += rectB.get_axes()

    for axis in axes:
        projection_a = rectA.project(axis)
        projection_b = rectB.project(axis)
        overlapping = overlap(projection_a, projection_b)
        if not overlapping:
            return False;
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
    return (n >= a) and (n <= b);

def overlap(a, b):
    if contains(a[0], b) or contains(a[1], b) or \
        contains(b[0], a) or contains(b[1], a):
        return True
    return False;

#TODO almost all functions also work in a polygon setting aswell
class rect(object):
    def __init__(self,center_x, center_y, width, height, theta):

        # compute vertexes on rect frame of reference (center is origin)
        # axis perpendicular to normals of the rect
        # vertexes clock-wise starting with bottom-left
        # bottom-right, top-right, top-left
        self.vertexes = np.array(\
                        [[- width/2, width/2, width/2, - width/2],
                        [- height/2,- height/2, height/2,  height/2]])
        
        self.vertexes = rect.rotate(self.vertexes, theta)
        self.vertexes = rect.translate(self.vertexes,center_x,center_y)


    def __call__(self):
        for i in range(4):
            plt.plot([self.vertexes[0][i-1],self.vertexes[0][i]], 
            [self.vertexes[1][i-1],self.vertexes[1][i]],'k-', lw=2)

    # index = 0 is first edge,1 second-edge
    def edge_direction(self,index):
        return (self.vertexes[:,index%len(self.vertexes[0,:])] - \
         self.vertexes[:,(index+1) % len(self.vertexes[0,:])])

    def vertices_to_edges(self):
        self.edges = [self.edge_direction(i) for i in range(len(self.vertexes[0,:]))]

    def get_axes(self):
        self.vertices_to_edges()
        return [orthogonal(edge) for edge in self.edges]
    
    # No need to normalize
    def project(self, axis):
        dots = [np.dot(axis, self.vertexes)]
        return [np.min(dots), np.max(dots)]

    # T = R
    @classmethod
    def rotate(cls, matrix, theta):
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta),  np.cos(theta)]])
        return np.matmul(rotation_matrix,matrix)
    
    # T = M
    @classmethod
    def translate(cls, matrix, dx, dy):
        matrix = np.append(matrix,[[1,1,1,1]],axis=0)
        translation_matrix = np.array([[1,0,dx],
                                       [0,1,dy]])
        matrix = np.matmul(translation_matrix,matrix)
        return matrix[:,:4]
    
    # T = M^(-1) * R * M
    # Inverse of translation is equal to -dx, -dy
    @classmethod
    def transform(cls,matrix, center_x, center_y, theta):
        matrix = rect.translate(matrix,-center_x,-center_y)
        matrix = rect.rotate(matrix,theta)
        matrix = rect.translate(matrix,center_x,center_y)
        return matrix

if __name__ == '__main__':
    
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect='equal')
    ax.grid(color='r', linestyle='-', linewidth=1)
    ax.set_xlim([-2,2])
    ax.set_ylim([-2,2])
    rectA = rect(0,0,1,2,45*pi/180)
    rectB = rect(1,1,1,1,0*pi/180)

    if(SAT(rectA, rectB)): print("colliding")
    else: print("not colliding")
    rectA()
    rectB()
    plt.show()
    
