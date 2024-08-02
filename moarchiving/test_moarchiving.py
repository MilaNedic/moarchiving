from moarchiving import MOArchive
from hv_plus import calc_hypervolume_3D

import unittest
import numpy as np
import os


def list_to_set(lst):
    return set([tuple(p) for p in lst])


class MyTestCase(unittest.TestCase):
    def test_hypervolume_3D(self):
        # loop over all files in the tests folder that contain "_3d_" in their name
        print(f"{'file name':20} |   new hv   |   old hv   |")

        for f_name in os.listdir('tests'):
            if "_3d_" not in f_name:
                continue
            # read the data points and the reference point from the file

            data_points = np.loadtxt(f"tests/{f_name}", delimiter=' ')
            infos = [str(p) for p in data_points.tolist()]
            ref_point = [1, 1, 1]

            # calculate the hypervolume using the new implementation
            moa = MOArchive(data_points, ref_point, infos)
            hv_new = moa.hypervolume

            # calculate the hypervolume using the old implementation
            hv_old = calc_hypervolume_3D(data_points, ref_point)

            # compare the hypervolumes
            print(f"{f_name:20} | {hv_new:.8f} | {hv_old:.8f} |")

            # assert hyper volumes are equal
            self.assertAlmostEqual(hv_new, hv_old, places=8)
            # assert infos are stored correctly
            self.assertEqual([str(p[:3]) for p in moa.points_list], moa.infos_list)

    def test_infos_non_dominated_3D(self):
        """ test if the infos are stored correctly - if the points are non dominated,
        the infos should be the same"""
        points = [
            [1, 2, 3],
            [3, 2, 1],
            [2, 3, 1],
            [1, 3, 2]
        ]
        infos = [str(p) for p in points]

        moa = MOArchive(points, [6, 6, 6], infos)
        # assert that the infos are stored in the same order as the points
        self.assertEqual([str(p[:3]) for p in moa.points_list], moa.infos_list)
        # assert that all the points in the archive are non dominated and thus have the same info
        self.assertSetEqual(set([str(p) for p in points]), set(moa.infos_list))

    def test_infos_dominated_3D(self):
        """ test if the infos about dominated points are removed """
        points = [
            [1, 2, 3],
            [3, 2, 1],
            [2, 3, 4],
            [2, 1, 0]
        ]
        infos = ["A", "B", "C", "D"]

        moa = MOArchive(points, [6, 6, 6], infos)
        # assert that only points A and D are stored in the archive
        self.assertSetEqual({"A", "D"}, set(moa.infos_list))

    def test_in_domain_3D(self):
        """ test if the in_domain function works correctly for 3D points"""
        ref_point = [6, 6, 6]
        moa = MOArchive([[1, 1, 1]], ref_point)

        # test if the points are in the domain
        self.assertTrue(moa.in_domain([1, 2, 3]))
        self.assertTrue(moa.in_domain([5.9, 5.9, 5.9]))
        # test if the point is not in the domain
        self.assertFalse(moa.in_domain([7, 8, 9]))
        self.assertFalse(moa.in_domain([6, 6, 6]))
        self.assertFalse(moa.in_domain([0, 0, 6]))

    def test_in_domain_4D(self):
        """ test if the in_domain function works correctly for 4D points"""
        ref_point = [6, 6, 6, 6]
        moa = MOArchive([[1, 1, 1, 1]], ref_point)

        # test if the points are in the domain
        self.assertTrue(moa.in_domain([1, 2, 3, 4]))
        self.assertTrue(moa.in_domain([5.9, 5.9, 5.9, 5.9]))
        # test if the point is not in the domain
        self.assertFalse(moa.in_domain([7, 8, 9, 10]))
        self.assertFalse(moa.in_domain([6, 6, 6, 6]))
        self.assertFalse(moa.in_domain([0, 0, 0, 6]))

    def test_add_3D(self):
        """ test if the add_points function works correctly for 3D points"""
        ref_point = [6, 6, 6]
        start_points = [[1, 2, 5], [3, 5, 1], [5, 1, 4]]
        moa = MOArchive(start_points, ref_point)

        # add point that is not dominated and does not dominate any other point
        u1 = [2, 3, 3]
        moa.add(u1)
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points_list))

        # add point that is dominated by another point in the archive
        u2 = [4, 5, 2]
        moa.add(u2)
        self.assertSetEqual(list_to_set(start_points + [u1]), list_to_set(moa.points_list))

        # add point that dominates another point in the archive
        u3 = [3, 1, 2]
        moa.add(u3)
        self.assertSetEqual(list_to_set(start_points[:2] + [u1, u3]), list_to_set(moa.points_list))

    def test_hypervolume_after_add_3D(self, n_points=1000, n_tests=10):
        ref_point = [1, 1, 1]

        for t in range(n_tests):
            np.random.seed(t)
            points = np.round(np.random.rand(n_points, 3), 3).tolist()
            infos = [str(p) for p in range(n_points)]
            moa = MOArchive(points, ref_point, infos=infos)
            true_hv = moa.hypervolume

            moa_add = MOArchive(points[:1], ref_point, infos=infos[:1])
            for i in range(1, n_points):
                moa_add.add(points[i], infos[i])

            self.assertAlmostEqual(moa_add.hypervolume, true_hv, places=6)

    def test_dominates(self):
        ref_point = [6, 6, 6]
        points = [[1, 3, 5], [5, 3, 1], [4, 4, 4]]
        moa = MOArchive(points, ref_point)

        # test that the points that are already in the archive are dominated
        for p in points:
            self.assertTrue(moa.dominates(p))

        # test other dominated points
        self.assertTrue(moa.dominates([5, 5, 5]))
        self.assertTrue(moa.dominates([2, 4, 5]))

        # test non dominated points
        self.assertFalse(moa.dominates([3, 3, 3]))
        self.assertFalse(moa.dominates([2, 5, 4]))
        self.assertFalse(moa.dominates([5, 1, 3]))

    def test_dominators(self):
        ref_point = [6, 6, 6]
        points = [[1, 2, 3], [3, 1, 2], [2, 3, 1], [3, 2, 1], [2, 1, 3], [1, 3, 2]]
        moa = MOArchive(points, ref_point)

        # test that the points that are already in the archive are dominated by itself
        for p in points:
            self.assertEqual([p], moa.dominators(p))
            self.assertEqual(1, moa.dominators(p, number_only=True))

        # test other dominated points
        self.assertEqual(list_to_set([[1, 2, 3], [2, 3, 1], [2, 1, 3], [1, 3, 2]]),
                         list_to_set(moa.dominators([2, 3, 4])))
        self.assertEqual(4, moa.dominators([2, 3, 4], number_only=True))

        self.assertEqual([], moa.dominators([2, 2, 2]))
        self.assertEqual(0, moa.dominators([2, 2, 2], number_only=True))

        self.assertEqual(list_to_set(points), list_to_set(moa.dominators([3, 3, 3])))
        self.assertEqual(6, moa.dominators([3, 3, 3], number_only=True))

    def test_distance_to_hypervolume_area(self):
        moa = MOArchive()
        self.assertEqual(0, moa.distance_to_hypervolume_area([1, 1, 1]))

        moa.reference_point = [2, 2, 2]
        # for points in the hypervolume area, the distance should be 0
        self.assertEqual(0, moa.distance_to_hypervolume_area([0, 0, 0]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([1, 1, 1]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([2, 2, 2]))
        self.assertEqual(0, moa.distance_to_hypervolume_area([0, 1, 2]))

        # for points outside the hypervolume area, the distance should be the Euclidean distance
        # to the hypervolume area
        self.assertEqual(1, moa.distance_to_hypervolume_area([2, 2, 3]))
        self.assertEqual(1, moa.distance_to_hypervolume_area([2, 0, 3]))
        self.assertEqual(10, moa.distance_to_hypervolume_area([0, 0, 12]))

        self.assertAlmostEqual(np.sqrt(2), moa.distance_to_hypervolume_area([0, 3, 3]), places=6)
        self.assertAlmostEqual(np.sqrt(2), moa.distance_to_hypervolume_area([2, 3, 3]), places=6)
        self.assertAlmostEqual(np.sqrt(3), moa.distance_to_hypervolume_area([3, 3, 3]), places=6)
        self.assertAlmostEqual(np.sqrt(147), moa.distance_to_hypervolume_area([9, 9, 9]), places=6)


if __name__ == '__main__':
    unittest.main()
