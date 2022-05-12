Examples
============================================

The following guide provides some examples as to how to use the API Wrapper.

Usage
------------------

Print the names of all TruckersMP servers.

.. code-block:: python

   import asyncio
   from truckersmp import TruckersMP

   loop = asyncio.get_event_loop()

   async def main():
      truckersmp = TruckersMP()
      servers = await truckersmp.get_servers()
      for server in servers:
         print(server.name)

   loop.run_until_complete(main())

Print the ID and names for all VTC IDs in tuple.

.. code-block:: python

   import asyncio
   from truckersmp import TruckersMP

   loop = asyncio.get_event_loop()

   async def main():
      truckersmp = TruckersMP()
      vtc_ids = (4, 5, 7)  # Each unique ID will result in an API call.
      tasks = [truckersmp.get_vtc(vtc_id) for vtc_id in vtc_ids]
      vtcs = await asyncio.gather(*tasks)  # The script will wait here until all API calls are made.
      for vtc in vtcs:
         print(f"ID {vtc.id} = {vtc.name}")

   loop.run_until_complete(main())

Error Handling
------------------

.. note::
   This part of documentation is incomplete

Print all the reasons user ID 924220 has been banned.

*With defaults:*


*All autohandlers disabled:*



Initialisation Per Use
------------------------------------

Initalising the class per use means that the cache and rate limiting features won't work as intended.

**The following is bad:**

.. code-block:: python

   servers = await TruckersMP().get_servers()
   version = await TruckersMP().get_version()

Instead do this:

.. code-block:: python

   truckersmp = TruckersMP()
   servers = await truckersmp.get_servers()
   version = await truckersmp.get_version()


**For a more real-world example:**

*This will make 5 API calls...*

.. code-block:: python

   for i in range(5):
      await TruckersMP().get_servers()

*This will make 1 API call, cache the result and serve that for the 4 other calls.
It will also execute far faster, assuming the API response time is similar.*

.. code-block:: python

   truckersmp = TruckersMP()  # You should only do this one in your program/script
   for i in range(5):
      await truckersmp.get_servers()