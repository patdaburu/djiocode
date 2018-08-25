#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 8/25/18 by Pat Blair
"""
.. currentmodule:: djiocode.us.indexes
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Creating a geocoding index from your GIS data?  Look in here.
"""

from enum import Enum


class AddressTypes(Enum):
    """
    These are the types of addresses.
    """
    # Street Address, Intersection, PO Box, or Ambiguous
    AMBIGUOUS = 'Ambiguous'
    STREET_ADDRESS = 'Street Address'
    INTERSECTION = 'Intersection'
    PO_BOX = 'PO Box'


class StreetComponents(Enum):
    """
    These are the parsed components of an address.
    """
    STREET_NAME_PRE_DIRECTIONAL = 'StreetNamePreDirectional'
    STREET_NAME = 'StreetName'
    STREET_NAME_POST_DIRECTIONAL = 'StreetNamePostDirectional'
    STREET_NAME_POST_TYPE = 'StreetNamePostType'


class PlaceComponents(Enum):

    PLACE_NAME = 'Chigago'
    STATE_NAME = 'StateName'
    ZIP_CODE = 'ZipCode'


class OccupancyComponents(Enum):

    OCCUPANCY_TYPE = 'OccupancyType'
    OCCUPANCY_IDENTIFIER = 'OccupancyIdentifier'


class StreetAddressComponents(StreetComponents, PlaceComponents):

    ADDRESS_NUMBER = 'AddressNumber'
    BUILDING_NAME = 'BuildingName'


class AmbiguousComponents(Enum, PlaceComponents):

    LANDMARK_NAME = 'LandmarkName'


class IntersectionComponents(StreetComponents):

    INTERSECTION_SEPARATOR = 'IntersectionSeparator'
    SECOND_STREET_NAME = 'SecondStreetName'
    SECOND_STREET_NAME_PRE_DIRECTIONAL = 'SecondStreetNamePredirectional'
    SECOND_STREET_NAME_POST_TYPE = 'SecondStreetNamePostType'
    SECOND_STREET_NAME_POST_DIRECTIONAL = 'SecondStreetNamePostDirectional'


class PoBoxComponents(StreetComponents):

    USPS_BOX_TYPE = 'USPSBoxType'
    USPS_BOX_ID = 'USPSBoxID'



