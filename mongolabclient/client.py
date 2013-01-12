# -*- coding: utf-8 *-*
try:
    import simplejson as json
except ImportError:
    import json
import urllib
import urllib2
from mongolabclient import settings, validators, errors, json_util


class MongoLabClient(object):
    """Instance class with the API key located at
    https://mongolab.com/user?username=[username].

    .. note::
       The ``version`` parameter is optional, because it is planed for using in
       future versions of REST API.

    When your connection needs to set a proxy, you can to set an `str` with the
    Proxy url to ``proxy_url`` parameter. If you don't set a ``proxy_url``,
    then :class:`MongoLabClient` gets system proxy settings.

    .. code-block:: python

       >>> from mongolabclient import MongoLabClient
       >>> MongoLabClient("MongoLabAPIKey", proxy_url="https://127.0.0.1:8000")
       MongoLabClient('MongoLabAPIKey', 'v1')
    """

    def __init__(self, api_key, version=settings.VERSION_1, proxy_url=None):
        self.api_key = api_key
        self.settings = settings.MongoLabSettings(version)
        self.__content_type = 'application/json;charset=utf-8'
        if proxy_url:
            self.__proxy_handler = urllib2.ProxyHandler({"https": proxy_url})
        else:
            self.__proxy_handler = urllib2.ProxyHandler()
        if not self.__validate_api_key():
            raise errors.InvalidAPIKey(self.api_key)

    def __validate_api_key(self):
        """Validate API Key format and make a GET request to REST API base url:
        https://api.mongolab.com/api/1"""
        if not validators.check_api_key(self.api_key):
            raise errors.BadAPIKeyFormat(self.api_key)
        r = self.__get_response(settings.VAL_API)
        return (r["status"] == 200)

    @property
    def base_url(self):
        """REST API base url depending selected version."""
        if not hasattr(self, "_base_url"):
            self._base_url = self.settings.base_url
        return self._base_url

    @property
    def proxy_handler(self):
        """"""
        return self.__proxy_handler

    def __get_full_url(self, operation, slug_params):
        """Returns full url of the operation selected with the slug parameters
        included."""
        return (self.base_url + operation["slug"]) % slug_params

    def __get_response(self, operation, slug_params={}, **kwargs):
        """Returns response of HTTP request depending the operation
        selected."""
        operation = self.settings.operations[operation]
        url = self.__get_full_url(operation, slug_params)
        if operation["method"] == "GET":
            kwargs["apiKey"] = self.api_key
            params = urllib.urlencode(kwargs)
            req = urllib2.Request(url + "?%s" % params)
        elif operation["method"] == "POST":
            params = kwargs.get("data", {})
            req = urllib2.Request(url + "?apiKey=%s" % self.api_key)
            req.add_header("Content-Type", self.__content_type)
            req.add_data(json.dumps(params, default=json_util.default))
        elif operation["method"] == "PUT":
            params = kwargs["data"]
            kwargs["apiKey"] = self.api_key
            del kwargs["data"]
            qs = urllib.urlencode(kwargs)
            req = urllib2.Request(url + "?%s" % qs)
            req.add_header("Content-Type", self.__content_type)
            req.add_data(json.dumps(params, default=json_util.default))
            req.get_method = lambda: operation["method"]
        else:
            kwargs["apiKey"] = self.api_key
            params = urllib.urlencode(kwargs)
            req = urllib2.Request(url + "?%s" % params)
            req.get_method = lambda: operation["method"]
        opener = urllib2.build_opener(self.proxy_handler)
        urllib2.install_opener(opener)
        try:
            f = opener.open(req)
            return {"status": f.getcode(), "result": json.loads(f.read(),
                object_hook=json_util.object_hook)}
        except urllib2.HTTPError, e:
            return {"status": e.getcode(), "result": json.loads(e.read(),
                object_hook=json_util.object_hook)}

    def list_databases(self):
        """Returns a list of databases name of your account.

        .. code-block:: bash

           GET /databases"""
        r = self.__get_response(settings.LST_DBS)
        if r["status"] == 200:
            return r["result"]
        raise Exception(r["result"]["message"])

    def list_collections(self, database):
        """Returns a list of collections name of database selected.

        .. code-block:: bash

           GET /databases/{database}/collections
        """
        r = self.__get_response(settings.LST_COLS, {"db": database})
        if r["status"] == 200:
            return r["result"]
        raise Exception(r["result"]["message"])

    def list_documents(self, database, collection, **kwargs):
        """Returns a list of dicts with the matched documents with the query.

        .. code-block:: bash

           GET /databases/{database}/collections/{collection}"""
        kwargs = validators.check_list_documents_params(**kwargs)
        r = self.__get_response(settings.LST_DOCS,
            {"db": database, "col": collection}, **kwargs)
        if r["status"] == 200:
            return r["result"]
        raise Exception(r["result"]["message"])

    def insert_documents(self, database, collection, doc_or_docs):
        """Insert a document or documents into collection.

        .. code-block:: bash

           POST /databases/{database}/collections/{collection}"""
        validators.check_documents_to_insert(doc_or_docs)
        r = self.__get_response(settings.INS_DOCS,
            {"db": database, "col": collection}, data=doc_or_docs)
        if r["status"] == 200:
            return r["result"]
        raise Exception(r["result"]["message"])

    def update_documents(self, database, collection, spec, doc_or_docs, upsert,
        multi):
        """Update a document or documents that matches with query. It is
        posible ``upsert`` data.

        .. code-block:: bash

           PUT /databases/{database}/collections/{collection}"""
        validators.check_document_to_update(doc_or_docs)
        r = self.__get_response(settings.UPD_DOCS,
            {"db": database, "col": collection},
            data=doc_or_docs, q=spec, m=multi, u=upsert)
        if r["status"] == 200:
            if r["result"]["error"]:
                raise Exception(r["result"]["error"])
            return r["result"]["n"]
        raise Exception(r["result"]["message"])

    def delete_replace_documents(self, database, collection, spec={},
        documents=[]):
        """Delete o replace a document or documents that matches with query.

        .. code-block:: bash

           PUT /databases/{database}/collections/{collection}"""
        r = self.__get_response(settings.DEL_REP_DOCS,
            {"db": database, "col": collection}, data=documents, q=spec)
        if r["status"] == 200:
            return r["result"]["n"]
        raise Exception(r["result"]["message"])

    def view_document(self, database, collection, _id):
        """Returns a dict with document matched with this ``_id``.

        .. code-block:: bash

           GET /databases/{database}/collections/{collection}/{_id}"""
        r = self.__get_response(settings.VIW_DOC,
            {"db": database, "col": collection, "id": str(_id)})
        if r["status"] == 200:
            return r["result"]
        raise Exception(r["result"]["message"])

    def update_document(self, database, collection, _id, document):
        """Update a document matched with this ``_id``, returns number of
        documents affected.

        .. code-block:: bash

           PUT /databases/{database}/collections/{collection}/{_id}"""
        r = self.__get_response(settings.UPD_DOC,
            {"db": database, "col": collection, "id": str(_id)},
            data=document)
        if r["status"] == 200:
            return r["result"]
        raise Exception(r["result"]["message"])

    def delete_document(self, database, collection, _id):
        """Delete a document matched with this ``_id``, returns a :class:`dict`
        with deleted document or a list of dicts with deleted documents.

        .. code-block:: bash

           DELETE /databases/{database}/collections/{collection}/{_id}"""
        r = self.__get_response(settings.DEL_DOC,
            {"db": database, "col": collection, "id": str(_id)})
        if r["status"] == 200:
            return r["result"]
        raise Exception(r["result"]["message"])

    def run_command(self, database, command):
        """Run a database-collection level command.

        .. code-block:: bash

           POST /databases/{database}/runCommand"""
        r = self.__get_response(settings.RUN_DB_COL_LVL_CMD, {"db": database},
            data=command)
        if r["status"] == 200:
            return r["result"]
        raise Exception(r["result"]["message"])
