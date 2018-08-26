#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 8/25/18 by Pat Blair
"""
.. currentmodule:: djiocode.us.indexes
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Creating a geocoding index from your GIS data?  Look in here.
"""

from collections import defaultdict
from enum import Enum
from typing import Any, Dict, Iterable
from postal.expand import expand_address
import usaddress
from.normalizers import directionals


class AddressTypes(Enum):
    """
    These are the types of addresses.
    """
    # Street Address, Intersection, PO Box, or Ambiguous
    Ambiguous = 'Ambiguous'
    StreetAddress = 'Street Address'
    Intersection = 'Intersection'
    POBox = 'PO Box'
#
#
# class StreetComponents(Enum):
#     """
#     These are the parsed components of an address.
#     """
#     STREET_NAME_PRE_DIRECTIONAL = 'StreetNamePreDirectional'
#     STREET_NAME = 'StreetName'
#     STREET_NAME_POST_DIRECTIONAL = 'StreetNamePostDirectional'
#     STREET_NAME_POST_TYPE = 'StreetNamePostType'
#
#
# class PlaceComponents(Enum):
#
#     PLACE_NAME = 'PlaceName'
#     STATE_NAME = 'StateName'
#     ZIP_CODE = 'ZipCode'
#
#
# class OccupancyComponents(Enum):
#
#     OCCUPANCY_TYPE = 'OccupancyType'
#     OCCUPANCY_IDENTIFIER = 'OccupancyIdentifier'
#
#
# class StreetAddressComponents(StreetComponents, PlaceComponents):
#
#     ADDRESS_NUMBER = 'AddressNumber'
#     BUILDING_NAME = 'BuildingName'
#
#
# class AmbiguousComponents(Enum, PlaceComponents):
#
#     LANDMARK_NAME = 'LandmarkName'
#
#
# class IntersectionComponents(StreetComponents):
#
#     INTERSECTION_SEPARATOR = 'IntersectionSeparator'
#     SECOND_STREET_NAME = 'SecondStreetName'
#     SECOND_STREET_NAME_PRE_DIRECTIONAL = 'SecondStreetNamePreDirectional'
#     SECOND_STREET_NAME_POST_TYPE = 'SecondStreetNamePostType'
#     SECOND_STREET_NAME_POST_DIRECTIONAL = 'SecondStreetNamePostDirectional'
#
#
# class POBoxComponents(StreetComponents):
#
#     USPS_BOX_TYPE = 'USPSBoxType'
#     USPS_BOX_ID = 'USPSBoxID'


class Details(Enum):
    AddressNumber = 'AddressNumber'
    AddressNumberPrefix = 'AddressNumberPrefix'
    AddressNumberSuffix = 'AddressNumberSuffix'
    BuildingName = 'BuildingName'
    CornerOf = 'CornerOf'
    IntersectionSeparator = 'IntersectionSeparator'
    LandmarkName = 'LandmarkName'
    NotAddress = 'NotAddress'
    OccupancyType = 'OccupancyType'
    OccupancyIdentifier = 'OccupancyIdentifier'
    PlaceName = 'PlaceName'
    Recipient = 'Recipient'
    StateName = 'StateName'
    StreetName = 'StreetName'
    StreetNamePreDirectional = 'StreetNamePreDirectional'
    StreetNamePreModifier = 'StreetNamePreModifier'
    StreetNamePreType = 'StreetNamePreType'
    StreetNamePostDirectional = 'StreetNamePostDirectional'
    StreetNamePostModifier = 'StreetNamePostModifier'
    StreetNamePostType = 'StreetNamePostType'
    SubaddressIdentifier = 'SubaddressIdentifier'
    SubaddressType = 'SubaddressType'
    USPSBoxGroupID = 'USPSBoxGroupID'
    USPSBoxGroupType = 'USPSBoxGroupType'
    USPSBoxID = 'USPSBoxID'
    USPSBoxType = 'USPSBoxType'
    ZipCode = 'ZipCode'
    SecondStreetName = 'SecondStreetName'
    SecondStreetNamePreDirectional = 'SecondStreetNamePreDirectional'
    SecondStreetNamePostType = 'SecondStreetNamePostType'
    SecondStreetNamePostDirectional = 'SecondStreetNamePostDirectional'


INTERSECTION_DETAILS = {
    Details.SecondStreetName,
    Details.SecondStreetNamePostDirectional,
    Details.SecondStreetNamePostType,
    Details.SecondStreetNamePostDirectional
}  #: a set of :py:class:`Details` values specific to intersections

DIRECTIONAL_DETAILS = {
    Details.StreetNamePreDirectional,
    Details.StreetNamePostDirectional,
    Details.SecondStreetNamePreDirectional,
    Details.SecondStreetNamePostDirectional
}  #: a set of :py:class:`Details` values that indicate directions


def is_directional(detail: Details):
    return detail in DIRECTIONAL_DETAILS


class ParseResult:
    """The result of a `usaddress` parse operation."""
    def __init__(self,
                 address_type: AddressTypes,
                 details: Dict[Details, Any]):
        self._address_type: AddressTypes = address_type
        self._details: Dict[Details, str] = defaultdict(
            lambda: None, details
        )  #: a dictionary of the details

    def address_type(self) -> AddressTypes:
        """Get the address type."""
        return self._address_type

    def detail(self, detail: Details):
        """Get the parsed value for a detail."""
        return self._details[detail]

    def details(self):
        """Get all the details as key-value pairs."""
        return self._details.items()

    def defines(self, detail: Details):
        """Is a particular detail defined?"""
        return detail in self._details

    def __repr__(self):
        details = ','.join(
            f'{k}={repr(v)}' for k, v in self._details.items()
        )
        return str(
            f"{self.__class__.__name__}(address_type={self._address_type}, "
            f"{details})"
        )


def expand(address: str) -> Iterable[str]:
    expands = set()
    for _expand in expand_address(address):
        # TODO: Eliminate near-duplicates.
        expands.add(_expand)
    return expands


def parse(address: str) -> ParseResult:
    """Parse an address."""
    _usaddress = usaddress.tag(address)

    details = {
        Details(k): v for k, v in _usaddress[0].items()
    }

    dir_details = {
        k: directionals.normalize(v)
        for k, v in details.items()
        if is_directional(k)
    }

    return ParseResult(
        address_type=AddressTypes(_usaddress[1]),
        details={
            **details,
            **dir_details
        }
    )

# PYPOSTAL:  https://github.com/openvenues/pypostal

# https://ispmarin.github.io/python-nltk/

# https://pypi.org/project/address/
# https://github.com/SwoopSearch/pyaddress