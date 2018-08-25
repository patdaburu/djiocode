#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 8/25/18 by Pat Blair
"""
.. currentmodule:: geocoding
.. moduleauthor:: Pat Daburu <pat@daburu.net>

All purpose functions and classes for geocoding.
"""

from abc import ABC
from typing import NamedTuple


class Location(NamedTuple):
    """
    A location is a coordinate in space.
    """
    x: float  #: the X coordinate
    y: float  #: the Y coordinate
    z: float or None  #: the Z coordinate (if there is one)
    srs: int  #: the spatial reference system of the coordinates


class GeocodeResult(NamedTuple):
    """
    A geocode result identifies a location with a label.
    """
    label: str
    location: Location


class Geocoder(ABC):
    """
    Geocoders find locations for addresses.
    """
    pass