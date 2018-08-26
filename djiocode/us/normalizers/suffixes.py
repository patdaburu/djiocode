#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 8/26/18 by Pat Blair
"""
.. currentmodule:: suffixes
.. moduleauthor:: Pat Blair <pblair@geo-comm.com>

This module deals with street suffixes (also known as "post type") according to
the USPS.
"""

import json
from pathlib import Path
import re
from typing import Iterable


_NOISE_CHARS = re.compile('\W', re.IGNORECASE)


class Abbrev:
    def __init__(self,
                 official: str,
                 common: Iterable[str]):
        self.official = official.lower()
        self.common = [c.lower() for c in common if c]


class Suffix:
    def __init__(self,
                 full: str,
                 abbrev: Abbrev):
        self.full = full.lower()
        self.abbrev = abbrev

    def __str__(self):
        return self.abbrev.official


class Suffixes:

    def __init__(self, suffixes: Path = None):
        sfx_path = (
            suffixes if suffixes
            else Path(__file__).resolve().parent / 'suffixes.json'
        )
        loaded = json.loads(sfx_path.read_text())
        self._dict = {
            full: Suffix(
                full=full,
                abbrev=Abbrev(
                    official=obj['abbrev']['official'],
                    common=obj['abbrev']['common'])
            )
            for full, obj in loaded.items()
        }
        # Create the dictionary that maps every common abbreviation to the
        # full name.
        self._commons = {}
        for sfx in self._dict.values():
            # Add the full name to the list (since it doesn't appear in the
            # list of common abbreviations).
            self._commons[sfx.full] = sfx
            # Add the common abbreviations.
            for common in sfx.abbrev.common:
                self._commons[common] = sfx

    @staticmethod
    def _sanitize(sfx: str) -> str or None:
        """

        :param sfx:
        :return:
        """
        if not sfx:
            return None
        _sfx = _NOISE_CHARS.sub('', sfx.lower())
        return _sfx if sfx else None

    def normal(self, sfx: str):
        """
        Get the normal for for a suffix.

        :param sfx: the suffix
        :return: the normal form (or `None` if no normal form is defined)
        """
        if not sfx:
            return None
        try:
            return self._commons[self._sanitize(sfx)]
        except KeyError:
            return None

    @classmethod
    def default(cls) -> 'Suffixes':
        """Get the default suffix set."""
        try:
            return getattr(cls, '__default__')
        except AttributeError:
            sfx = Suffixes()
            setattr(cls, '__default__', sfx)
            return sfx


def normalize(suffix: str) -> Suffix or None:
    """
    Normalize a suffix string.

    :param suffix: the suffix string
    :return: the normal form (or `None` if no normal form is defined)
    """
    if not suffix:
        return None
    try:
        return Suffixes.default().normal(suffix)
    except KeyError:
        return None
