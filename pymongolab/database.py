# -*- coding: utf-8 *-*
from pymongolab import collection


class Database(object):
    """For instance this class, you needs an instance of
    :class:`pymongolab.connection.MongoClient` and the name of your database.

    Example usage:

    .. code-block:: python

       >>> from pymongolab import MongoClient, database
       >>> con = MongoClient("MongoLabAPIKey")
       >>> database.Database(con, "database")
       Database(MongoClient('MongoLabAPIKey', 'v1'), 'database')

    Easy usage (Attibute-style access):

    .. code-block:: python

       >>> from pymongolab import MongoClient
       >>> con = MongoClient("MongoLabAPIKey")
       >>> con.database
       Database(MongoClient('MongoLabAPIKey', 'v1'), 'database')

    Easy usage (Dictionary-style access):

    .. code-block:: python

       >>> from pymongolab import MongoClient
       >>> con = MongoClient("MongoLabAPIKey")
       >>> con["database"]
       Database(MongoClient('MongoLabAPIKey', 'v1'), 'database')
    """

    def __init__(self, connection, name):
        self.__connection = connection
        self.name = name

    @property
    def connection(self):
        """An instance of :class:`pymongolab.connection.MongoClient` used for
        internal calls to MongoLab REST API via :mod:`mongolabclient`.
        """
        return self.__connection

    def __eq__(self, other):
        if isinstance(other, Database):
            us = (self.connection, self.name)
            them = (other.connection, other.name)
            return us == them
        return NotImplemented

    def __repr__(self):
        return "Database(%r, %r)" % (self.connection, self.name)

    def __getattr__(self, name):
        """Get a collection using a attribute-style access.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> db = con.database
           >>> db.collection
           Collection(Database(MongoClient('MongoLabAPIKey', 'v1'),
           'database'), 'collection')
        """
        return collection.Collection(self, name)

    def __getitem__(self, name):
        """Get a database using a dictionary-style access.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> db = con["database"]
           >>> db["collection"]
           Collection(Database(MongoClient('MongoLabAPIKey', 'v1'),
           'database'), 'collection')
        """
        return self.__getattr__(name)

    def collection_names(self):
        """Returns a list with the collection names of your database.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database.collection_names()
           [u'collection', u'users', u'issues']
        """
        return self.connection.request.list_collections(self.name)

    def command(self, command, value=1):
        """Execute a database-collection level command via
        :func:`mongolabclient.client.MongoLabClient.run_command`. The supported
        methods are listed on MongoLab API Documentation:
        https://support.mongolab.com/entries/20433053-rest-api-for-mongodb

        Example usage:

        A command like ``{dbstats: 1}`` can be sent using:

        .. code-block:: python

           >>> db.command("dbStats")

        For a command where the value matters, like ``{collstats:
        collection_name}`` we can do:

        .. code-block:: python

           >>> db.command("collStats", collection_name)

        Full example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database.command("dbStats")
           {u'storageSize': 57344, u'serverUsed': u'dsXXXXXX-b.mongolab.com',
           u'ok': 1.0, u'avgObjSize': 101.88235294117646, u'db': u'dbname',
           u'indexes': 7, u'objects': 34, u'collections': 9,
           u'fileSize': 16777216, u'numExtents': 9, u'dataSize': 3464,
           u'indexSize': 57232, u'nsSizeMB': 16}
           >>>
           >>> con.database.command("collStats", "collectionname")
           {u'count': 7, u'ns': u'dbname.collectionname',
           u'serverUsed': u'dsXXXXXX-b.mongolab.com', u'lastExtentSize': 8192,
           u'avgObjSize': 258.85714285714283, u'totalIndexSize': 8176,
           u'systemFlags': 1, u'ok': 1.0, u'userFlags': 0, u'numExtents': 1,
           u'nindexes': 1, u'storageSize': 8192,
           u'indexSizes': {u'_id_': 8176},
           u'paddingFactor': 1.0020000000000007, u'size': 1812}
        """
        if isinstance(command, basestring):
            command = {command: str(value)}
        return self.connection.request.run_command(self.name, command)
