# -*- coding: utf-8 *-*
from mongolabclient import errors
import re


__api_key_re = re.compile(r"^[a-z0-9]{24}|[a-zA-Z0-9_-]{32}$")

__param_types = {"spec": dict, "count": bool, "fields": dict, "find_one": bool,
    "sort": dict, "skip": int, "limit": int}
__default_params = {"spec": {}, "count": False, "fields": {},
    "find_one": False, "sort": {}, "skip": 0, "limit": 0}
__key_params = {"spec": "q", "count": "c", "fields": "f", "find_one": "fo",
    "sort": "s", "skip": "sk", "limit": "l"}

__update_operators = ["$inc", "$set", "$unset", "$push", "$pushAll",
    "$addToSet", "$each", "$pop", "$pull", "$pullAll", "$rename", "$bit"]


def check_api_key(api_key):
    """Check if API key match with the following regular expression:
    :regexp:`[a-z0-9]{24}`."""
    return not (__api_key_re.match(api_key) is None)


def check_database_name(name):
    """Check if database name contains invalid characteres."""
    if not name:
        raise errors.InvalidName("Database name cannot be the empty string.")
    for invalid_char in [" ", ".", "$", "/", "\\", "\x00"]:
        if invalid_char in name:
            raise errors.InvalidName("Database name cannot contain the "
                "character %r" % invalid_char)


def check_list_documents_params(**kwargs):
    """Check parameters for REST API list-documents operation evaluating if
    they are correct, removing them if no have a value or raise a TypeError if
    they have a not expected type."""
    params = {}
    keys = __param_types.keys() + __default_params.keys() + __key_params.keys()
    for key, value in kwargs.iteritems():
        if key not in keys:
            raise Exception("Invalid parameter %r" % (key))
        if not isinstance(value, __param_types[key]):
            raise TypeError("%r must be an instance of %r" % (key,
                __param_types[key].__name__))
        if value != __default_params[key]:
            params[__key_params[key]] = value
    return params


def remove_empty_params(params):
    """Remove items from a :class:`dict` if no have a value."""
    r = {}
    for key, value in params.iteritems():
        if value:
            r[key] = value
    return r


def check_documents_to_insert(doc_or_docs):
    """Check if :class:`dict` item type is an instance of list or an instance
    of :class:`dict`."""
    if not isinstance(doc_or_docs, dict) and not isinstance(doc_or_docs, list):
        raise TypeError("doc_or_docs must be an instance of dict or list")


def check_document_to_update(document):
    """Check if the update operators from a document are valid."""
    for key in document.keys():
        if not key in __update_operators:
            raise errors.InvalidUpdateOperator(key)
