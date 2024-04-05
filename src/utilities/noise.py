"""This module initializes and optimizes the opensimplex noise module."""

from __future__ import annotations

import sys
import random

from numba import njit

from opensimplex.internals import _noise2, _noise3, _init

from src.constants.world_constants import (
    CHUNK_SIZE,
    NOISE_FACTOR,
    NOISE_OCTAVES,
    NOISE_PERSISTENCE,
    NOISE_EXPONENT,
    NOISE_AMPLITUDE,
    WORLD_DEPTH,
    WORLD_WIDTH,
)

perm, perm_grad_index3 = _init(seed=random.randint(0, sys.maxsize))


@njit
def get_noise_2d(x: float, y: float) -> float:
    """Return the 2d noise value. Most likely used to generate a height map
    value.

    Args:
        x (float): The x coordinate.
        y (float): The y coordinate.

    Returns:
        float: The 2d noise value.
    """

    return _noise2(x, y, perm)


@njit
def get_noise_3d(x: float, y: float, z: float) -> float:
    """Return the 3d noise value. Most likely used to compute which voxels are
    needed in the context of cave generation.

    Args:
        x (float): The x coordinate.
        y (float): The y coordinate.
        z (float): The z coordinate.

    Returns:
        float: The 3d noise value.
    """

    return _noise3(x, y, z, perm, perm_grad_index3)


@njit
def simplex_noise_2d(x: float, y: float) -> float:
    """Returns the height map for the given x, y coordinates. The parameters
    can be adjusted to get the desired height map, or terrain. Utilises the
    performance boost from the njit decorator.

    Args:
        x (float): The x coordinate for noise sampling.
        y (float): The y coordinate for noise sampling.

    Returns:
        float: The noise value.
    """

    x = NOISE_FACTOR * x / (WORLD_WIDTH * CHUNK_SIZE)
    y = NOISE_FACTOR * y / (WORLD_DEPTH * CHUNK_SIZE)

    noise = 0
    frequency_sum = 0

    for i in range(NOISE_OCTAVES):
        amplitude = NOISE_PERSISTENCE * pow(2, i)
        frequency = 1.0 / amplitude

        dx = amplitude * x
        dy = amplitude * y

        noise += frequency * get_noise_2d(dx, dy)
        frequency_sum += frequency

    return int(pow(noise / frequency_sum, NOISE_EXPONENT) * NOISE_AMPLITUDE)
