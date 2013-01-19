# -*- coding: utf-8 *-*
"""Bits and pieces used by the REST client that don't really fit elsewhere."""

from collections import OrderedDict


def _index_document(index_list):
    """Helper to generate an index specifying document.

    Takes a list of (key, direction) pairs.
    """
    if isinstance(index_list, dict):
        raise TypeError("passing a dict to sort/create_index/hint is not "
                        "allowed - use a list of tuples instead. did you "
                        "mean %r?" % list(index_list.iteritems()))
    elif not isinstance(index_list, list):
        raise TypeError("must use a list of (key, direction) pairs, "
                        "not: " + repr(index_list))
    if not len(index_list):
        raise ValueError("key_or_list must not be the empty list")

    index = OrderedDict()
    for (key, value) in index_list:
        if not isinstance(key, basestring):
            raise TypeError("first item in each key pair must be a string")
        if not isinstance(value, (basestring, int)):
            raise TypeError("second item in each key pair must be ASCENDING, "
                            "DESCENDING, GEO2D, GEOHAYSTACK, TEXT, or other "
                            "valid MongoDB index specifier.")
        index[key] = value
    return index
