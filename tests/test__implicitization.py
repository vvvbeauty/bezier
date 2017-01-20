# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np

from tests import utils


class Test__evaluate3(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(nodes, x_val, y_val):
        from bezier import _implicitization

        return _implicitization._evaluate3(nodes, x_val, y_val)

    @staticmethod
    def _compute_expected(x_val, y_val):
        return 289.0 * (
            ((17.0 * x_val - 81.0) * x_val + 135.0) * x_val - 27.0 * y_val)

    def test_it(self):
        # f(x, y) = 289(17 x^3 - 81 x^2 + 135 x - 27 y)
        nodes = np.asfortranarray([
            [0.0, 0.0],
            [1.0, 5.0],
            [2.0, 1.0],
            [3.0, 5.0],
        ])

        local_eps = 0.5**26  # sqrt(machine precision)

        xy_vals = utils.get_random_nodes(
            shape=(50, 2), seed=81390, num_bits=8)
        for x_val, y_val in xy_vals:
            result = self._call_function_under_test(nodes, x_val, y_val)
            expected = self._compute_expected(x_val, y_val)
            self.assertAlmostEqual(result, expected, delta=local_eps)


class Test_evaluate(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(nodes, x_val, y_val):
        from bezier import _implicitization

        return _implicitization.evaluate(nodes, x_val, y_val)

    def test_point(self):
        nodes = np.asfortranarray([[1.0, 1.0]])
        with self.assertRaises(ValueError):
            self._call_function_under_test(nodes, 0.0, 0.0)

    def test_linear(self):
        # f(x, y) = -4 x + y + 3
        nodes = np.asfortranarray([
            [1.0, 1.0],
            [2.0, 5.0],
        ])

        result0 = self._call_function_under_test(nodes, 0.0, 0.0)
        self.assertEqual(result0, 3.0)
        result1 = self._call_function_under_test(nodes, 0.0, 1.0)
        self.assertEqual(result1, 4.0)
        result2 = self._call_function_under_test(nodes, 1.0, 0.0)
        self.assertEqual(result2, -1.0)
        result3 = self._call_function_under_test(nodes, 1.0, 1.0)
        self.assertEqual(result3, 0.0)

        # f(x, y) = (-12 x + 8 y - 5) / 32
        nodes = np.asfortranarray([
            [0.0, 0.625],
            [0.25, 1.0],
        ])

        result0 = self._call_function_under_test(nodes, 0.0, 0.0)
        self.assertEqual(result0, -5.0 / 32)
        result1 = self._call_function_under_test(nodes, 0.0, 1.0)
        self.assertEqual(result1, 3.0 / 32)
        result2 = self._call_function_under_test(nodes, 1.0, 0.0)
        self.assertEqual(result2, -17.0 / 32)
        result3 = self._call_function_under_test(nodes, 1.0, 1.0)
        self.assertEqual(result3, -9.0 / 32)

        # f(x, y) = -x
        nodes = np.asfortranarray([
            [0.0, 0.0],
            [0.0, 1.0],
        ])

        vals = np.linspace(0.0, 1.0, 9)
        for x_val in vals:
            for y_val in vals:
                result = self._call_function_under_test(nodes, x_val, y_val)
                self.assertEqual(result, -x_val)

    def test_quadratic(self):
        # f(x, y) = x^2 + 4 x - 4 y
        nodes = np.asfortranarray([
            [0.0, 0.0],
            [1.0, 1.0],
            [2.0, 3.0],
        ])

        values = [
            self._call_function_under_test(nodes, 0.0, 0.0),
            self._call_function_under_test(nodes, 1.0, 0.0),
            self._call_function_under_test(nodes, 2.0, 0.0),
            self._call_function_under_test(nodes, 0.0, 1.0),
            self._call_function_under_test(nodes, 1.0, 1.0),
            self._call_function_under_test(nodes, 0.0, 2.0),
        ]
        expected = [0.0, 5.0, 12.0, -4.0, 1.0, -8.0]
        self.assertEqual(values, expected)

        # f(x, y) = (x - y)^2 - y
        nodes = np.asfortranarray([
            [0.75, 0.25],
            [-0.25, -0.25],
            [-0.25, 0.25],
        ])
        xy_vals = utils.get_random_nodes(
            shape=(50, 2), seed=7930932, num_bits=8)
        values = []
        expected = []
        for x_val, y_val in xy_vals:
            values.append(self._call_function_under_test(nodes, x_val, y_val))
            expected.append((x_val - y_val) * (x_val - y_val) - y_val)
        self.assertEqual(values, expected)

    def test_cubic(self):
        # f(x, y) = 13824 (x^3 - 24 y^2)
        nodes = np.asfortranarray([
            [6.0, -3.0],
            [-2.0, 3.0],
            [-2.0, -3.0],
            [6.0, 3.0],
        ])

        local_eps = 0.5**26  # sqrt(machine precision)

        xy_vals = utils.get_random_nodes(
            shape=(50, 2), seed=238382, num_bits=8)
        for x_val, y_val in xy_vals:
            result = self._call_function_under_test(nodes, x_val, y_val)
            expected = 13824.0 * (x_val * x_val * x_val - 24.0 * y_val * y_val)
            self.assertAlmostEqual(result, expected, delta=local_eps)

    def test_quartic(self):
        # f(x, y) = -28 x^4 + 56 x^3 - 36 x^2 + 8 x - y
        nodes = np.asfortranarray([
            [0.0, 0.0],
            [0.25, 2.0],
            [0.5, -2.0],
            [0.75, 2.0],
            [1.0, 0.0],
        ])

        with self.assertRaises(NotImplementedError):
            self._call_function_under_test(nodes, 0.0, 0.0)


class Test_eval_intersection_polynomial(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(nodes1, nodes2, t):
        from bezier import _implicitization

        return _implicitization.eval_intersection_polynomial(
            nodes1, nodes2, t)

    def test_degrees_1_1(self):
        # f1(x, y) = (8 y - 3) / 8
        nodes1 = np.asfortranarray([
            [0.0, 0.375],
            [1.0, 0.375],
        ])
        # x2(t), y2(t) = 1 / 2, 3 s / 4
        nodes2 = np.asfortranarray([
            [0.5, 0.0],
            [0.5, 0.75],
        ])

        values = [
            self._call_function_under_test(nodes1, nodes2, 0.0),
            self._call_function_under_test(nodes1, nodes2, 0.5),
            self._call_function_under_test(nodes1, nodes2, 1.0),
        ]
        # f1(x2(t), y2(t)) = 3 (2 t - 1) / 8
        expected = [-0.375, 0.0, 0.375]
        self.assertEqual(values, expected)

    def test_degrees_1_2(self):
        # f1(x, y) = 2 (4 x + 3 y - 24)
        nodes1 = np.asfortranarray([
            [0.0, 8.0],
            [6.0, 0.0],
        ])
        # x2(t), y2(t) = 9 t, 18 t (1 - t)
        nodes2 = np.asfortranarray([
            [0.0, 0.0],
            [4.5, 9.0],
            [9.0, 0.0],
        ])

        values = [
            self._call_function_under_test(nodes1, nodes2, 0.0),
            self._call_function_under_test(nodes1, nodes2, 0.25),
            self._call_function_under_test(nodes1, nodes2, 0.5),
            self._call_function_under_test(nodes1, nodes2, 0.75),
            self._call_function_under_test(nodes1, nodes2, 1.0),
        ]
        # f1(x2(t), y2(t)) = 12 (4 - 3 t) (3 t - 1)
        expected = [-48.0, -9.75, 15.0, 26.25, 24.0]
        self.assertEqual(values, expected)


class Test__to_power_basis11(utils.NumPyTestCase):

    @staticmethod
    def _call_function_under_test(nodes1, nodes2):
        from bezier import _implicitization

        return _implicitization._to_power_basis11(nodes1, nodes2)

    def test_it(self):
        # f1(x, y) = -(12 x - 8 y + 5) / 32
        nodes1 = np.asfortranarray([
            [0.0, 0.625],
            [0.25, 1.0],
        ])
        # x2(t), y2(t) = (2 - 3 t) / 4, (3 t + 2) / 4
        nodes2 = np.asfortranarray([
            [0.5, 0.5],
            [-0.25, 1.25],
        ])
        # f1(x2(t), y2(t)) = (15 t - 7) / 32
        result = self._call_function_under_test(nodes1, nodes2)
        expected = np.array([-7.0, 15.0]) / 32.0
        self.assertEqual(result, expected)


class Test_to_power_basis(utils.NumPyTestCase):

    @staticmethod
    def _call_function_under_test(nodes1, nodes2):
        from bezier import _implicitization

        return _implicitization.to_power_basis(nodes1, nodes2)

    def test_degrees_1_1(self):
        # f1(x, y) = -x
        nodes1 = np.asfortranarray([
            [0.0, 0.0],
            [0.0, 1.0],
        ])
        # x2(t), y2(t) = 1, t
        nodes2 = np.asfortranarray([
            [1.0, 0.0],
            [1.0, 1.0],
        ])
        # f1(x2(t), y2(t)) = -1
        result = self._call_function_under_test(nodes1, nodes2)
        expected = np.array([-1.0, 0.0])
        self.assertEqual(result, expected)

    def test_unsupported(self):
        nodes_yes = np.zeros((2, 2), order='F')
        nodes_no = np.zeros((3, 2), order='F')

        with self.assertRaises(NotImplementedError):
            self._call_function_under_test(nodes_yes, nodes_no)

        with self.assertRaises(NotImplementedError):
            self._call_function_under_test(nodes_no, nodes_no)