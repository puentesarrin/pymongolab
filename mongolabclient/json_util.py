# -*- coding: utf-8 *-*
from datetime import datetime
from bson.objectid import ObjectId


def object_hook(dct):
    """This is a loads hook for JSON deserialize, converting a :class:`dict`
    field to an instance of :class:`bson.objectid.ObjectId` or an instance
    of :class:`datetime.datetime`."""
    if "$oid" in dct:
        return ObjectId(dct["$oid"])
    if "$date" in dct:
        return datetime.strptime(dct["$date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return dct


def default(obj):
    """This is a dumps hook for JSON serialize, converting to an instance of
    :class:`bson.objectid.ObjectId` or an instance of
    :class:`datetime.datetime`."""
    if isinstance(obj, ObjectId):
        return {"$oid": str(obj)}
    if isinstance(obj, datetime):
        return {"$date": datetime.strftime(obj, "%Y-%m-%dT%H:%M:%S.%fZ")}
    raise TypeError("%r is not JSON serializable" % obj)
