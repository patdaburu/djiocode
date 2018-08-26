#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path

import json
path = '/home/pblair/Documents/usps_streets.csv'


all = {}
current = None

with open(str(path)) as inin:
    for line in inin.readlines():
        parts = line.replace('\xa0', '')[:-1].split(',')
        parts = [part.lower() for part in parts if part]

        if len(parts) == 3:
            current = {
                'full': parts[0],
                'abbrev': {
                    'official': parts[2],
                    'common': [parts[2], parts[1]]
                }
            }
            all[parts[0]] = current
        else:
            current['abbrev']['common'].append(parts[0])

print(json.dumps(all, indent=4))