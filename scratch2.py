#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 8/25/18 by Pat Blair
"""
.. currentmodule:: scratch2
.. moduleauthor:: Pat Blair <pblair@geo-comm.com>

This module needs a description.
"""
from djiocode.us.usaddress import parse
from djiocode.us.normalizers import directionals

#parsed = parse('123 main street, emeryville, california')

# for p in parse('123 main street, emeryville, california'):
#     print(p)



p =parse('123 N Main st. Southwest, emeryville, california')
print(p)


print(directionals.normalize('South-West'))
print(directionals.normalize('north east'))