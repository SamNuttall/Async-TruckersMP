Async-TruckersMP
============================================

An asynchronous Python API wrapper for `TruckersMP`_.

.. warning::
    This library is in alpha and bugs may still be present.

Features
------------------

* **Rate limiting** - Pre-emptive rate limiting so you'll never hit a 429.
* **Caching** - Automatic caching of responses so you don't have to.
* **Configurable** - Several configuration options on initialisation.
* **Documented** - Full docs with examples included for reference.
* **Data models** - API responses are parsed into objects (Python classes).

Usage
------------------

Install
^^^^^^^^^^^^^

Install via pip using either of these methods:

.. code-block::

   pip install async-truckersmp


.. code-block::

   pip install git+https://github.com/SamNuttall/Async-TruckersMP.git

Quickstart
^^^^^^^^^^^^^

Let's write a script to print all the server names.

.. code-block:: python

   from truckersmp import TruckersMP  # Import the library

   loop = asyncio.get_event_loop()  # Get the asyncio event loop

   async def main():
       truckersmp = TruckersMP()  # Initalise the TruckersMP class
       servers = await truckersmp.get_servers()  # Call the get_servers method
       for server in servers:  # Loop through each server
           print(server.name)  # Get the name of the server and print it

   loop.run_until_complete(main())  # Run the main function


Resources & Support
---------------------

* `Documentation`_.
* `Github Repository`_.
* If you need further help, feel free to contact Sam#9210 on Discord or open a new issue.

Licence
------------------
Released under the `MIT License`_.

.. _TruckersMP: https://truckersmp.com/
.. _Documentation: https://async-truckersmp.readthedocs.io/
.. _Github Repository: https://github.com/SamNuttall/Async-TruckersMP
.. _MIT License: https://github.com/SamNuttall/Async-TruckersMP/blob/main/LICENSE
