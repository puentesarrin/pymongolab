# -*- coding: utf-8 *-*
from pymongolab import collection


class Database(object):
    """For instance this class, you needs an instance of
    :class:`pymongolab.connection.Connection` and the name of your database.

    Example usage:

    .. code-block:: python

       >>> from pymongolab import Connection, database
       >>> con = Connection("MongoLabAPIKey")
       >>> database.Database(con, "database")
       Database(Connection('MongoLabAPIKey', 'v1'), 'database')

    Easy usage (Attibute-style access):

    .. code-block:: python

       >>> from pymongolab import Connection
       >>> con = Connection("MongoLabAPIKey")
       >>> con.database
       Database(Connection('MongoLabAPIKey', 'v1'), 'database')

    Easy usage (Dictionary-style access):

    .. code-block:: python

       >>> from pymongolab import Connection
       >>> con = Connection("MongoLabAPIKey")
       >>> con["database"]
       Database(Connection('MongoLabAPIKey', 'v1'), 'database')
    """

    def __init__(self, connection, name):
        self.__connection = connection
        self.name = name

    @property
    def connection(self):
        """An instance of :class:`pymongolab.connection.Connection` used for
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

           >>> from pymongolab import Connection
           >>> con = Connection("MongoLabAPIKey")
           >>> db = con.database
           >>> db.collection
           Collection(Database(Connection('MongoLabAPIKey', 'v1'),
           'database'), 'collection')
        """
        return collection.Collection(self, name)

    def __getitem__(self, name):
        """Get a database using a dictionary-style access.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import Connection
           >>> con = Connection("MongoLabAPIKey")
           >>> db = con["database"]
           >>> db["collection"]
           Collection(Database(Connection('MongoLabAPIKey', 'v1'),
           'database'), 'collection')
        """
        return self.__getattr__(name)

    def collection_names(self):
        """Returns a list with the collection names of your database.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import Connection
           >>> con = Connection("MongoLabAPIKey")
           >>> con.database.collection_names()
           [u'collection', u'users', u'issues']
        """
        return self.connection.request.list_collections(self.name)

    def command(self, command):
        """Execute a database-collection level command via
        :func:`mongolabclient.client.MongoLabClient.run_command`.
        """
        return self.connection.request.run_command(\
            self.database.name, command
        )
