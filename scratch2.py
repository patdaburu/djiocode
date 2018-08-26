#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 8/25/18 by Pat Blair
"""
.. currentmodule:: scratch2
.. moduleauthor:: Pat Blair <pblair@geo-comm.com>

This module needs a description.
"""
from djiocode.us.usaddress import parse

parsed = parse('123 main street, emeryville, california')

print(parsed)