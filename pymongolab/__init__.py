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


from pymongolab.connection import Connection
from pymongolab.mongo_client import MongoClient
