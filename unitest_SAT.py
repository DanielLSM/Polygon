import unittest
import numpy as np
from SAT_many_rectangles import Rectangle, check_collisions, SAT
import matplotlib.pyplot as plt
from matplotlib import patches

# The answer to life, universe and everything
SEED = 42
np.random.seed(SEED)


def plt_rects(rects, show=False):
    fig, ax = plt.subplots()
    for rect in rects:
        poly = patches.Polygon(rect.points, fill=False)
        ax.add_patch(poly)
    ax.autoscale_view()
    ax.set_aspect('equal', 'datalim')
    plt.savefig('figure.png')
    if show:
        plot.show()


def check_collisions_brute(rects):
    overlaps = []
    for i, rect in enumerate(rects):
        for other_rect in rects[i + 1:]:
            if SAT(rect, other_rect):
                overlaps.append((rect.id, other_rect.id))
    return overlaps


def is_equal(o1, o2):
    if len(o1) != len(o2):
        return False
    for i, pair in enumerate(o1):
        if pair[0] > pair[1]:
            o1[i] = (pair[1], pair[0])
    for i, pair in enumerate(o2):
        if pair[0] > pair[1]:
            o2[i] = (pair[1], pair[0])
    o1.sort()
    o2.sort()
    return o1 == o2


def create_rectangles(size, max_origin=100, max_dim=10, axis_aligned=False):
    x = np.random.randint(max_origin, size=size)
    y = np.random.randint(max_origin, size=size)
    if not axis_aligned:
        dx = 2 * np.random.rand(size) - 1
        dy = 2 * np.random.rand(size) - 1
    else:
        dx = np.random.randint(2, size=size)
        dy = 1 - dx
    width = np.random.randint(max_dim - 1, size=size) + 1
    length = np.random.randint(max_dim - 1, size=size) + 1
    ids = np.arange(size)
    rects = [
        Rectangle(x[i], y[i], dx[i], dy[i], width[i], length[i], i)
        for i in ids
    ]
    return rects


class TestCollisions(unittest.TestCase):
    def test_large_random(self):
        rects = create_rectangles(1000, max_origin=1000, max_dim=20)
        o2 = check_collisions_brute(rects)
        o1 = check_collisions(rects)
        self.assertTrue(is_equal(o1, o2))

    def test_axis_aligned(self):
        rects = create_rectangles(
            100, max_origin=100, max_dim=4, axis_aligned=True)
        o1 = check_collisions(rects)
        o2 = check_collisions_brute(rects)
        self.assertTrue(is_equal(o1, o2))


if __name__ == '__main__':
    unittest.main()
