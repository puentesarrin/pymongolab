CHANGELOG
=========

1.2 (2013-02-19)
----------------

* Fixed and improved ``command`` method from ``Database`` class using
  ``OrderedDict``.
* Added support for ``last_status``, ``previous_error``, ``error``,
  ``reset_error_history``, ``profiling_level`` and ``set_profiling_level``
  methods to ``Database`` class.
* Added support for ``distinct``, ``reindex`` and ``find_and_modify`` methods
  to ``Collection`` class.
* Added ``helpers`` module.
* Added UTF-8 support for REST API requests.
* Support for new API key format.


1.1 (2012-12-14)
----------------

* Added support for `MongoClient`_.
* Improved usage examples on documentation.

.. _MongoClient: http://blog.mongodb.org/post/36666163412/introducing-mongoclient


1.0rc1 (2012-08-15)
-------------------

* Initial release.
