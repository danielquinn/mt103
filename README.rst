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
        mt103.text.bank_operation_code,
        mt103
    ))


Installation
------------

It's on PyPi, so just install it with pip.

.. code-block:: shell

    $ pip install mt103


TODO
----

Parsing MT103 messages should work just fine and you should be able to access
all of the components via the Python API *except* for section ``13C``.  From
the specs I've seen, it's unclear as to whether this section is permitted to
repeat (meaning it should be parsed as a list) or if it's one value only.  If
someone can explain this authoritatively to me, I can include support for this
section as well.