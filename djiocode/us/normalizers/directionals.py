#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 8/26/18 by Pat Blair
"""
.. currentmodule:: directionals
.. moduleauthor:: Pat Blair <pblair@geo-comm.com>

South-West, SouthWest, SW... it's all the same.
"""

from enum import Enum
import re
from typing import Dict, Set


_NOISE_CHARS = re.compile('\W', re.IGNORECASE)


class CardinalDirections(Enum):
    NORTH = 'N'
    EAST = 'E'
    WEST = 'W'
    SOUTH = 'S'
    NORTHEAST = 'NE'
    NORTHWEST = 'NW'
    SOUTHEAST = 'SE'
    SOUTHWEST = 'SW'

    def __str__(self):
        return self.value


def normals(lib: Dict[CardinalDirections, Set[str]]):
    _normals = dict()
    for cd, syn in lib.items():
        for _syn in syn:
            _normals[_syn] = cd
    return _normals


_NORMALS = normals({
    CardinalDirections.NORTH: {'north', 'n'},
    CardinalDirections.EAST: {'east', 'e'},
    CardinalDirections.WEST: {'west', 'w'},
    CardinalDirections.SOUTH: {'south', 's'},
    CardinalDirections.NORTHEAST: {'northeast', 'ne'},
    CardinalDirections.NORTHWEST: {'northwest', 'nw'},
    CardinalDirections.SOUTHEAST: {'southeast', 'se'},
    CardinalDirections.SOUTHWEST: {'southwest', 'sw'}
})


def _sanitize(directional: str) -> str or None:
    """Clean up a directional string for comparison."""
    if not directional:
        return None
    return _NOISE_CHARS.sub('', directional.lower())


def normalize(directional: str) -> CardinalDirections or None:
    """Normalize a directional string."""
    if not directional:
        return None
    try:
        return _NORMALS[_sanitize(directional)]
    except KeyError:
        return None
