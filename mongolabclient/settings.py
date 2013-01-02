# -*- coding: utf-8 *-*
from mongolabclient import errors

VAL_API = "validate-api-key"
"""Pseudo-code for Validation API key operation."""
LST_DBS = "list-databases"
"""Pseudo-code for List databases operation."""
LST_COLS = "list-collections"
"""Pseudo-code for List collection operation."""
LST_DOCS = "list-documents"
"""Pseudo-code for List documents operation."""
INS_DOCS = "insert-multiple-documents"
"""Pseudo-code for Insert multiple documents operation. This code supports
insert a single document too"""
UPD_DOCS = "update-multiple-documents"
"""Pseudo-code for Update multiple documents operation."""
DEL_REP_DOCS = "deletereplace-multiple-documents"
"""Pseudo-code for Delete & replace multiple documents operation."""
VIW_DOC = "view-document"
"""Pseudo-code for View document operation."""
UPD_DOC = "update-document"
"""Pseudo-code for Update document operation."""
DEL_DOC = "delete-document"
"""Pseudo-code for Delete document operation."""
RUN_DB_COL_LVL_CMD = "run-database-collection-level-commands"
"""Pseudo-code for Run Database-collection level commands operation."""

VERSION_1 = "v1"
"""Pseudo-code for MongoLab REST API version."""


class MongoLabSettings(object):
    """Instance class to get url and operations detail depending the version
    REST API.

    All of this data are specified on MongoLab Support website:
    http://support.mongolab.com/entries/20433053-rest-api-for-mongodb

    .. note::
       The ``version`` parameter is optional, because it is planed for using in
       future versions of REST API.
    """

    __BASE_URLS = {VERSION_1: "https://api.mongolab.com/api/1/"}

    __OPERATIONS = {
        VERSION_1: {
            VAL_API: {
                "method": "GET",
                "slug": ""},
            LST_DBS: {
                "method": "GET",
                "slug": "databases"},
            LST_COLS: {
                "method": "GET",
                "slug": "databases/%(db)s/collections"},
            LST_DOCS: {
                "method": "GET",
                "slug": "databases/%(db)s/collections/%(col)s"},
            INS_DOCS: {
                "method": "POST",
                "slug": "databases/%(db)s/collections/%(col)s"},
            UPD_DOCS: {
                "method": "PUT",
                "slug": "databases/%(db)s/collections/%(col)s"},
            DEL_REP_DOCS: {
                "method": "PUT",
                "slug": "databases/%(db)s/collections/%(col)s"},
            VIW_DOC: {
                "method": "GET",
                "slug": "databases/%(db)s/collections/%(col)s/%(id)s"},
            UPD_DOC: {
                "method": "PUT",
                "slug": "databases/%(db)s/collections/%(col)s/%(id)s"},
            DEL_DOC: {
                "method": "DELETE",
                "slug": "databases/%(db)s/collections/%(col)s/%(id)s"},
            RUN_DB_COL_LVL_CMD: {
                "method": "POST",
                "slug": "databases/%(db)s/runCommand"}
            }
        }

    def __init__(self, version=VERSION_1):
        if not version in self.__BASE_URLS.keys():
            raise errors.UnsupportedVersion()
        self.version = version
        self.base_url = self.__BASE_URLS[version]
        self.operations = self.__OPERATIONS[version]
