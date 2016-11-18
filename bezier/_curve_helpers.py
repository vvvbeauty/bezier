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

"""Private helper methods for B |eacute| zier curves.

.. |eacute| unicode:: U+000E9 .. LATIN SMALL LETTER E WITH ACUTE
   :trim:
"""


import six


def de_casteljau_one_round(nodes, s):
    r"""Performs one "round" of the de Casteljau algorithm for curves.

    Converts the ``nodes`` into a basis for a surface one degree smaller
    by using the barycentric weights:

    .. math::

       q_{i, j} = (1 - s) \cdot p_{i + 1, j} + s \cdot p_{i, j + 1}

    Args:
        nodes (numpy.ndarray): The nodes to reduce.
        s (float): Parameter along the reference interval.

    Returns:
        numpy.ndarray: The converted nodes.
    """
    return (1.0 - s) * nodes[:-1, :] + s * nodes[1:, :]


def de_casteljau(nodes, degree, s):
    r"""Performs the de Casteljau algorithm for curves.

    Successively calls :func:`de_casteljau_one_round` until the
    ``nodes`` have been combined into a single point on the curve.

    Args:
        nodes (numpy.ndarray): The nodes defining a curve.
        degree (int): The degree of the curve (assumed to be one less than
            the number of ``nodes``.
        s (float): Parameter along the reference interval.

    Returns:
        numpy.ndarray: The evaluated point on the curve.
    """
    value = nodes
    for _ in six.moves.xrange(degree):
        value = de_casteljau_one_round(value, s)

    # Here: Value will be 1x2, we just want the 1D point.
    return value.flatten()
