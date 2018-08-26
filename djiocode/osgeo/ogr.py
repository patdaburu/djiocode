#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 8/25/18 by Pat Blair
"""
.. currentmodule:: djiocode.osgeo.ogr
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Handy tools to know when you're working with
`GDAL <https://pcjericks.github.io/py-gdalogr-cookbook/>`_ geometries and
data sources.
"""

import multiprocessing as mp
from pathlib import Path
from typing import Any, Callable, Iterable, List
import numpy as np
from osgeo import ogr


def opends(path: Path) -> ogr.DataSource:
    """
    Open a GDAL/OGR data source.

    :param path: the path to the data source
    :return:
    """
    return ogr.Open(str(path))


def _apply(path: Path,
           layer: str,
           func: Callable[[ogr.Feature], Any],
           fids: Iterable[int]) -> List[Any]:
    """
    This is the function

    :param path: the path to the data source
    :param layer: the name of the layer in which the features reside
    :param func: the function to apply to each feature
    :param fids: the feature IDs against which the function shall be applied
    :return: an iteration of the results of each function call

    .. seealso::

        :py:func:`apply`
    """
    ds: ogr.DataSource = opends(path)
    layer: ogr.Layer = ds.GetLayerByName(layer)
    _fids = list(fids)
    # Create a list to hold the outputs (one per feature ID).
    outputs = [None] * len(_fids)
    # Apply the function to each feature.
    for idx, fid in enumerate(_fids):
        feature: ogr.Feature = layer.GetFeature(fid)
        outputs[idx] = func(feature)
    # Clean up.
    ds.Destroy()
    # Return what we got.
    return outputs


def apply(
        path: Path,
        func: Callable[[ogr.Feature], Any],
        layers: Iterable[str]=None,
        procs: int = None) -> Iterable[Any]:
    """
    Apply a function asynchronously to the features in an OGR data source.
    
    :param path: the path to the data source
    :param func: the function to apply
    :param layers: the layers to which the function should apply
    :param procs: the number of processes
    :return: the results
    """
    ds: ogr.DataSource = opends(path=path)
    _layers: List[ogr.Layer] = (
        list(layers) if layers
        else [layer.GetName() for layer in ds]
    )
    # How many times do we divide up the work?
    _split = procs if procs else mp.cpu_count()

    # Create a list to hold all the output as it is collected.
    _all_output = []

    for layer in _layers:
        _layer = ds.GetLayerByName(layer)
        # How many features do we have?
        fcount = _layer.GetFeatureCount()
        # Split up the feature count that many times to determine how many
        # features will be evaluated in a single process.
        divvy = int(fcount/_split)

        # Create a table to hold all the fids.  (The number of rows is
        # equivalent to the number of processes, and the number of columns
        # is the number of feature IDs we're going to give to each process.)
        fids = np.empty([_split, divvy], dtype=int)
        fids.fill(-1)  # FID values are not negative.
        _col = 0  # Keep track of what we have.
        _row = 0
        for feature in _layer:
            fid = feature.GetFID()
            if _col >= divvy:
                # Reset.
                _col = 0
                _row += 1
            fids[_row, _col] = fid
            _col += 1


        # TODO: Optimize the last set!  Don't waste a process on 1 or 2 records.

        # Create pool to do the work.
        pool = mp.Pool(processes=_split)
        # Run the processes and retrieve the results.
        results = [
            pool.apply_async(
                func=_apply,
                args=(
                    path,
                    layer,
                    func,
                    [f for f in _fids if f >= 0]
                )
            ) for _fids in fids
        ]
        # Retrieve the outputs.
        _outputs = [p.get() for p in results]
        # The outputs are lists of lists, so...
        for outputs in _outputs:
            # ...drill down to the individual input item...
            for output in outputs:
                # ...and return the output.
                yield output

        # Close the pool.
        pool.close()  #: TODO... can we use the same pool?
        # Wait.
        pool.join()
    # Clean up.
    ds.Destroy()
