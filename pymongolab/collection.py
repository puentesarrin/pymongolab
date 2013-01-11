# -*- coding: utf-8 *-*
from pymongolab import cursor
from bson.objectid import ObjectId


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

    @property
    def database(self):
        """An instance of :class:`pymongolab.database.Database` used for
        internal calls to MongoLab REST API via :mod:`mongolabclient`.
        """
        return self.__database

    def __eq__(self, other):
        if isinstance(other, Collection):
            us = (self.database, self.name)
            them = (other.database, other.name)
            return us == them
        return NotImplemented

    def __repr__(self):
        return "Collection(%r, %r)" % (self.database, self.name)

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
