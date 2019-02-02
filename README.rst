mt103
=====

Parse MT103 messages from the Swift payments network

What's an MT103?
----------------

Banks don't really deal with cash much any more.  Instead, they push bits
around the internet tracking where your money goes digitally.  The network that
handles much of that movement is called `Swift`_, and the transfers are
documented in a special format native to that network called *MT103*.

.. _Swift: https://en.wikipedia.org/wiki/ISO_9362


What's this Do?
---------------

Unfortunately, MT103 isn't a common standard for most software developers.
It's ugly & hard to read for humans and not at all easy to parse.  This library
attempts to fix that, so all you have to do is pass an MT103 string into it and
you get back a native Python object with the properties you're looking for.

.. code-block:: python

    from mt103 import MT103

    mt103 = MT103("some-mt-103-string")
    print("basic header: {}, bank op code: {}, complete message: {}".format(
        mt103.basic_header,
        mt103.text.bank_operation_code
        mt103
    ))


Installation
------------

It's on PyPi, so just install it with pip.

.. code-block:: shell

    $ pip install mt103


Changelog
---------

1.0.0
.....

* Changed the nature of the ``.user_header`` attribute from a string to a
  ``UserHeader`` object.  This new object has the same string representation
  (``str(mt103.user_header)``), but now also possesses new sub-attributes.
* Added support for user header fields including ``bank_priority_code``
  (``bpc``), ``message_user_reference`` (``mur``), ``service_type_identifier``
  (``sti``), and ``unique_end_to_end_transaction_reference`` (``uetr``).


0.0.1
.....

Initial release.
