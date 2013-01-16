# -*- coding: utf-8 *-*
from pymongolab import database
from mongolabclient import MongoLabClient


class MongoClient(object):
    """Instance class with the API key located at
    https://mongolab.com/user?username=[username].

    Example usage:

    .. code-block:: python

       >>> from pymongolab import MongoClient
       >>> MongoClient("MongoLabAPIKey")
       MongoClient('MongoLabAPIKey', 'v1')

    .. note::
       The ``version`` parameter is optional, because it is planed for using in
       future versions of REST API.

    When your connection needs to set a proxy, you can to set an `str` with the
    Proxy url to ``proxy_url`` parameter. If you don't set a ``proxy_url``,
    then :class:`mongolabclient.client.MongoLabClient` gets system proxy
    settings.

    .. code-block:: python

       >>> from pymongolab import MongoClient
       >>> MongoClient("MongoLabAPIKey", proxy_url="https://127.0.0.1:8000")
       MongoClient('MongoLabAPIKey', 'v1')
    """

    def __init__(self, api_key, version="v1", proxy_url=None):
        self.api_key = api_key
        self.version = version
        self.__request = MongoLabClient(api_key, version, proxy_url)

    @property
    def request(self):
        """An instance of :class:`mongolabclient.client.MongoLabClient` used
        for internal calls to MongoLab REST API via :mod:`mongolabclient`.
        """
        return self.__request

    def __eq__(self, other):
        if isinstance(other, MongoClient):
            us = (self.api_key, self.version)
            them = (other.api_key, other.version)
            return us == them
        return NotImplemented

    def __repr__(self):
        return "MongoClient(%r, %r)" % (self.api_key, self.version)

    def __getattr__(self, name):
        """Get a database using a attribute-style access.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database
           Database(MongoClient('MongoLabAPIKey', 'v1'), 'database')
        """
        return database.Database(self, name)

    def __getitem__(self, name):
        """Get a database using a dictionary-style access.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> db = con["database"]
           Database(MongoClient('MongoLabAPIKey', 'v1'), 'database')
        """
        return self.__getattr__(name)

    def database_names(self):
        """Returns a list with your database names.

        Example usage:

        .. code-block:: python

           >>> from pymongolab import MongoClient
           >>> con = MongoClient("MongoLabAPIKey")
           >>> con.database_names()
           [u'database', u'otherdatabase']
        """
        return self.request.list_databases()
