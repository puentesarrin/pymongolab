Usage examples
==============

This tutorial is very similar to `PyMongo tutorial`_.

Making a connection
-------------------

The first step when working with **PyMongoLab** is to create an instance of
:class:`~pymongolab.mongo_client.MongoClient`. Doing so is easy:

.. code-block:: python

   >>> from pymongolab import MongoClient
   >>> MongoClient("MongoLabAPIKey")


Getting a database
------------------

When working with PyMongoLab you access databases using attribute style access
on :class:`~pymongolab.mongo_client.MongoClient` instances:

.. code-block:: python

   >>> db = con.test_database

Or (using dictionary style access):

.. code-block:: python

   >>> db = con.["test_database"]


Getting a collection
--------------------

Getting a collection in PyMongoLab works the same as getting a database:

.. code-block:: python

   >>> col = db.test_collection

Or (using dictionary style access):

.. code-block:: python

   >>> col = db["test_collection"]


Inserting a document
--------------------

To insert a document into a collection we can use the
:meth:`~pymongolab.collection.Collection.insert` method:

.. code-block:: python

   >>> posts = db.posts
   >>> post = col.insert({"title": "My new post"})
   >>> post
   {u'_id': ObjectId('50cb4c3ae4b04e114b81a4e0'), u'title': u'My new post'}


Bulk inserts
------------

In addition to inserting a single document, we can also perform *bulk insert*
operations, by passing an iterable as the first argument to
:meth:`~pymongolab.collection.Collection.insert`. This will insert each
document in the iterable:

.. code-block:: python

   >>> posts = db.posts
   >>> result = col.insert([{"title": "My first post"}, {"title": "My second post"}])
   >>> result
   {u'n': 2}


Getting single document
-----------------------

With :meth:`~pymongolab.collection.Collection.find_one` method returns a
single document matching a query (or ``None`` if there are no
matches). Here we use :meth:`~pymongolab.collection.Collection.find_one`
to get the first document from the posts collection:

.. code-block:: python

   >>> posts.find_one()
   {u'_id': ObjectId('50cb4c3ae4b04e114b81a4e0'), u'title': u'My new post'}

:meth:`~pymongo.collection.Collection.find_one` also supports querying
on specific elements that the resulting document must match. To limit
our results to a document with title "My first post" we do:

.. code-block:: python

   >>> posts.find_one({"title": "My first post"})
   {u'_id': ObjectId('50cb55c1d823707b91c04513'), u'title': u'My first post'}

If we try with a different title, like "My second post", we'll get no result:

.. code-block:: python

   >>> posts.find_one({"title": "My second post"})
   {u'_id': ObjectId('50cb55c1d823707b91c04514'), u'title': u'My second post'}


Querying for more than one document
-----------------------------------
To get more than a single document as the result of a query we use the
:meth:`~pymongolab.collection.Collection.find`
method. :meth:`~pymongolab.collection.Collection.find` returns a
:class:`~pymongolab.cursor.Cursor` instance, which allows us to iterate
over all matching documents. For example, we can iterate over every
document in the ``posts`` collection:

.. code-block:: python

   >>> for post in posts.find():
   ...   post
   ...
   {u'_id': ObjectId('50cb4c3ae4b04e114b81a4e0'), u'title': u'My new post'}
   {u'_id': ObjectId('50cb55c1d823707b91c04513'), u'title': u'My first post'}
   {u'_id': ObjectId('50cb55c1d823707b91c04514'), u'title': u'My second post'}

Just like we did with :meth:`~pymongolab.collection.Collection.find_one`,
we can pass a document to :meth:`~pymongo.collection.Collection.find`
to limit the returned results. Here, we get only those documents whose
title is "My first post":

.. code-block:: python

  >>> for post in posts.find({"title": "My first post"}):
  ...   post
  ...
   {u'_id': ObjectId('50cb55c1d823707b91c04513'), u'title': u'My first post'}


Counting documents
------------------

If we just want to know how many documents match a query we can
perform a :meth:`~pymongolab.cursor.Cursor.count` operation instead of a
full query. We can get a count of all of the documents in a
collection:

.. code-block:: python

   >>> posts.count()
   3

or just of those documents that match a specific query:

.. code-block:: python

   >>> posts.find({"title": "My first post"}).count()
   1


.. _PyMongo tutorial: http://api.mongodb.org/python/current/tutorial.html
