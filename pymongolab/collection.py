# -*- coding: utf-8 *-*
from bson.objectid import ObjectId
from collections import OrderedDict
from pymongolab import cursor, helpers


class Collection(object):
    """For instance this class, you needs an instance of
    :class:`pymongolab.database.Database` and the name of your collection.

    Example usage:

    .. code-block:: python

       >>> from pymongolab import MongoClient, database, collection
       >>> con = MongoClient("MongoLabAPIKey")
       >>> db = database.Database(con, "database")
       >>> collection.Collection(db, "collection")
       Collection(Database(MongoClient('MongoLabAPIKey', 'v1'),
       'database'), 'collection')

    Easy usage (Attibute-style access):

    .. code-block:: python

       >>> from pymongolab import MongoClient
       >>> con = MongoClient("MongoLabAPIKey")
       >>> db = con.database
       >>> db.collection
       Collection(Database(MongoClient('MongoLabAPIKey', 'v1'),
       'database'), 'collection')

    Easy usage (Dictionary-style access):

    .. code-block:: python

       >>> from pymongolab import MongoClient
       >>> con = MongoClient("MongoLabAPIKey")
       >>> db = con["database"]
       >>> db["collection"]
       Collection(Database(MongoClient('MongoLabAPIKey', 'v1'),
       'database'), 'collection')
    """

    def __init__(self, database, name):
        self.__database = database
        self.name = name
        self.__full_name = u"%s.%s" % (self.__database.name, self.name)

    @property
    def database(self):
        """An instance of :class:`pymongolab.database.Database` used for
        internal calls to MongoLab REST API via :mod:`mongolabclient`.
        """
        return self.__database

    @property
    def full_name(self):
        """The full name of this :class:`pymongolab.collection.Collection`.

        The full name is of the form `database_name.collection_name`.
        """
        return self.__full_name

    def __eq__(self, other):
        if isinstance(other, Collection):
            us = (self.database, self.name)
            them = (other.database, other.name)
            return us == them
        return NotImplemented

    def __repr__(self):
        return "Collection(%r, %r)" % (self.database, self.name)

    def __iter__(self):
        return self

    def next(self):
        raise TypeError("'Collection' object is not iterable")

    def find(self, spec_or_id=None, fields={}, skip=0, limit=0, **kwargs):
        """Query the database.

        Returns an instance of :class:`pymongolab.cursor.Cursor` with the
        result set.

        :Parameters:
            - `spec` (optional): a dict specifying elements which must be
              present for a document to be included in the result set
            - `fields` (optional): a dict specifying the fields to return
            - `sort` (optional): a list of (key, direction) pairs specifying
              the sort order for this query.
            - `skip` (optional): the number of documents to omit (from the
              start of the result set) when returning the results
            - `limit` (optional): the maximum number of results to return

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database.collection.find()
           <pymongolab.cursor.Cursor object at 0x1972490>
           >>> list(con.database.collection.find())
           [{u'_id': ObjectId('50243d38e4b00c3b3e75fc94'), u'foo': u'bar',
           u'tld': u'com'}, {u'_id': ObjectId('50004d646cf431171ed53846'),
           u'foo': u'bar', u'tld': u'org'}]
        """
        if isinstance(spec_or_id, ObjectId) or \
            isinstance(spec_or_id, basestring):
            return self.database.connection.request.view_document(
                self.database.name, self.name, spec_or_id)
        return cursor.Cursor(self, spec_or_id, fields, skip, limit, **kwargs)

    def find_and_modify(self, query={}, update=None, upsert=False, sort=None,
        **kwargs):
        """Update and return an object.

        This is a thin wrapper around the findAndModify_ command. The
        positional arguments are designed to match the first three arguments
        to :meth:`update` however most options should be passed as named
        parameters. Either `update` or `remove` arguments are required, all
        others are optional.

        Returns either the object before or after modification based on `new`
        parameter. If no objects match the `query` and `upsert` is false,
        returns ``None``. If upserting and `new` is false, returns ``{}``.

        :Parameters:
            - `query`: filter for the update (default ``{}``)
            - `update`: see second argument to :meth:`update` (no default)
            - `upsert`: insert if object doesn't exist (default ``False``)
            - `sort`: a list of (key, direction) pairs specifying the sort
              order for this query. See :meth:`~pymongo.cursor.Cursor.sort`
              for details.
            - `remove`: remove rather than updating (default ``False``)
            - `new`: return updated rather than original object
              (default ``False``)
            - `fields`: see second argument to :meth:`find` (default all)
            - `**kwargs`: any other options the findAndModify_ command
              supports can be passed here.

        .. _findAndModify: http://dochub.mongodb.org/core/findAndModify

        .. versionadded:: 1.2
        """
        if (not update and not kwargs.get('remove', None)):
            raise ValueError("Must either update or remove")
        if (update and kwargs.get('remove', None)):
            raise ValueError("Can't do both update and remove")
        if query:
            kwargs['query'] = query
        if update:
            kwargs['update'] = update
        if upsert:
            kwargs['upsert'] = upsert
        if sort:
            if isinstance(sort, list):
                kwargs['sort'] = helpers._index_document(sort)
            elif (isinstance(sort, OrderedDict) or isinstance(sort, dict) and
                 len(sort) == 1):
                kwargs['sort'] = sort
            else:
                raise TypeError("sort must be a list of (key, direction) "
                                "pairs, a dict of len 1, or an instance of "
                                "OrderedDict")
        out = self.database.command("findAndModify", self.name, **kwargs)
        if not out['ok']:
            if out["errmsg"] == "No matching object found":
                return None
            else:
                raise ValueError("Unexpected Error: %s" % (out,))
        return out.get('value')

    def find_one(self, spec_or_id=None, **kwargs):
        """Query the database.

        Return an instance of :class:`dict` with the first document of query
        result on None if no results.

        :Paramaters:
            - `spec_or_id` (optional): a dict specifying elements which must be
              present for a document to be included in the result set or a _id
              value.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database.collection.find_one()
           {u'_id': ObjectId('50243d38e4b00c3b3e75fc94'), u'foo': u'bar',
           u'tld': u'com'}
        """
        if isinstance(spec_or_id, ObjectId) or \
            isinstance(spec_or_id, basestring):
            return self.database.connection.request.view_document(
                self.database.name, self.name, spec_or_id)
        if not spec_or_id:
            spec_or_id = {}
        documents = self.find(spec_or_id, limit=1, **kwargs)
        if not documents.count():
            return None
        return documents[0]

    def count(self):
        """Returns the number of documents into a collection.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database.collection.count()
           22
        """
        return len(self.find())

    def distinct(self, key):
        """Get a list of distinct values for `key` among all documents in this
        collection.

        :Parameters:
            - `key`: name of key for which we want to get the distinct values.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database.collection.distinct("title")
           [u'first title', u'second title', u'my title', u'your title']

        .. versionadded:: 1.2
        """
        return self.database.command({'distinct': self.name,
                                      'key': key})['values']

    def insert(self, doc_or_docs):
        """Insert a document or documents into this collection.

        Example usage:

        .. code-block:: python

           >>> doc = {"foo": "bar"}
           >>> docs = [{"foo": "bar"}, {"foo": "bar"}]

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> #Inserting a document
           ... con.database.collection.insert(doc)
           {u'foo': u'bar', u'_id': ObjectId('50242e46e4b0926293fd4d7c')}
           >>> #Inserting documents
           ... con.database.collection.insert(docs)
           {u'n': 2}

        If you insert a document only, this function returns an instance of
        :class:`dict` of inserted document including as attribute `_id` an
        instance of :class:`bson.objectid.ObjectId`. Else, this function
        returns the number of inserted documents.
        """
        return self.database.connection.request.insert_documents(
            self.database.name, self.name, doc_or_docs)

    def update(self, spec, document, upsert=False, multi=False):
        """Update a document or documents into this collection.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> list(con.database.collection.find())
           [{u'_id': ObjectId('50243d38e4b00c3b3e75fc94'), u'foo': u'bar',
           u'tld': u'org'}]
           >>> con.database.collection.update({"foo": "bar"},
           ...    {"$set": {"tld": "com"}})
           1
           >>> list(con.database.collection.find())
           [{u'_id': ObjectId('50243d38e4b00c3b3e75fc94'), u'foo': u'bar',
           u'tld': u'com'}]
           >>> con.database.othercollection.update({"foo":"bar"},
           ...    {"$set": {"tld": "com"}}, multi=True)
           6

        .. warning::

           Update operation defaults affects to first document that matchs with
           `spec` parameter. Then for other usages it's better to use `multi`
           parameter on `True`.
        """
        return self.database.connection.request.update_documents(
            self.database.name, self.name, spec, document, upsert, multi)

    def reindex(self):
        """Rebuilds all indexes on this collection.

        .. warning:: reindex blocks all other operations (indexes
           are built in the foreground) and will be slow for large
           collections.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database.collection.reindex()
           {u'ok': 1.0, u'indexes': [{u'ns': u'mydb.mycoll', u'name': u'_id_',
           u'key': {u'_id': 1}}], u'msg': u'indexes dropped for collection',
           u'nIndexes': 1, u'nIndexesWas': 1.0}

        .. versionadded:: 1.2
        """
        result = self.database.command('reIndex', self.name)
        del result['serverUsed']
        return result

    def remove(self, spec_or_id=None):
        """Remove a document or documents into this collection.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> #Deleting a document
           ... con.database.collection.remove({"foo": "bar"})
           2
           >>> #Deleting all documents
           ... con.database.collection.remove()
           22
        """
        if isinstance(spec_or_id, ObjectId) or \
            isinstance(spec_or_id, basestring):
            return self.database.connection.request.delete_document(
                self.database.name, self.name, spec_or_id)
        if not spec_or_id:
            spec_or_id = {}
        return self.database.connection.request.delete_replace_documents(
            self.database.name, self.name, spec_or_id, [])
