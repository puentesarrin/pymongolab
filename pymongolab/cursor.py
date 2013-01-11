# -*- coding: utf-8 *-*


class Cursor(object):
    """A cursor / iterator over MongoLab REST API query results.
    """

    def __init__(self, collection, spec_or_id=None, fields={}, skip=0, limit=0,
        **kwargs):
        self.collection = collection
        if not spec_or_id:
            spec_or_id = {}
        kwargs["spec"] = spec_or_id
        kwargs["fields"] = fields
        kwargs["skip"] = skip
        kwargs["limit"] = limit
        r = self.collection.database.connection.request
        self.__data = r.list_documents(self.collection.database.name,
            self.collection.name, **kwargs)
        self.__index = 0
        self.__count = len(self.__data)

    def __getitem__(self, index_or_slice):
        if isinstance(index_or_slice, int) or \
            isinstance(index_or_slice, slice):
            return self.__data[index_or_slice]
        raise TypeError("index_or_slice must be an instance of int or slice")

    def __iter__(self):
        return self

    def __len__(self):
        return self.__count

    def next(self):
        """Iterate the current cursor with result set."""
        if self.__index >= self.__count:
            raise StopIteration
        item = self.__data[self.__index]
        self.__index += 1
        return item

    def count(self):
        """Get the size of the results set for this query."""
        return self.__count
