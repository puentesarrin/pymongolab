# -*- coding: utf-8 *-*
"""PyMongo_-flavored package for accessing to MongoLab databases via
`MongoLabClient`.

.. _PyMongo: http://api.mongodb.org/python/current/"""


ASCENDING = 1
"""Ascending sort order."""
DESCENDING = -1
"""Descending sort order."""


OFF = 0
"""No database profiling."""
SLOW_ONLY = 1
"""Only profile slow operations."""
ALL = 2
"""Profile all operations."""


version_tuple = (1, 2, '+')


def get_version_string():
    if isinstance(version_tuple[-1], basestring):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))

version = get_version_string()


from pymongolab.connection import Connection
from pymongolab.mongo_client import MongoClient
