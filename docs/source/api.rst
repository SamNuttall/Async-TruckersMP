API Reference
==============

Base
--------------
The base class can be imported and used like so:

.. code-block:: python

   from truckersmp import TruckersMP
   truckersmp = TruckersMP()


.. autoclass:: truckersmp.base.TruckersMP

Get Player
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_player

Get Bans
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_bans

Get Servers
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_servers

Get In-game Time
^^^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_ingame_time

Get Events
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_events

Get Event
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_event

Get VTCs
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtcs

Get VTC
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtc

Get VTC News
^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtc_news

Get a VTC News Post
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtc_news_post

Get VTC Roles
^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtc_roles

Get a VTC Role
^^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtc_role

Get VTC Members
^^^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtc_members

Get a VTC Member
^^^^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtc_member

Get VTC Events
^^^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_vtc_events

Get Version
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_version

Get Rules
^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP.get_rules

_process_request function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: truckersmp.base.TruckersMP._process_request

Models
--------------
Below all the models can be found. These are classes that are often returned when using the base class.

Example use of a Model:

.. code-block:: python

   """This will print the names of all the admins that have banned the user with id 924220"""
   from truckersmp import TruckersMP
   truckersmp = TruckersMP()
   user_id = 924220
   bans = truckersmp.get_bans(user_id)  # Returns a list of Ban objects (model)
   for ban in bans:
       print(ban.admin_name)

Ban
^^^^^^^^^^^^^^
.. currentmodule:: models.ban
.. autoclass:: Ban()

Events
^^^^^^^^^^^^^^
.. currentmodule:: models.event
.. autoclass:: Events()

Event
^^^^^^^^^^^^^^
.. currentmodule:: models.event
.. autoclass:: Event()

EventType
+++++++++++++
.. currentmodule:: models.event.Event
.. autoclass:: EventType()

Server
+++++++++++++
.. autoclass:: Server()

Departure
+++++++++++++
.. autoclass:: Departure()

Arrive
+++++++++++++
.. autoclass:: Arrive()

VTC
+++++++++++++
.. autoclass:: VTC()

User
+++++++++++++
.. autoclass:: User()


Attendances
+++++++++++++
.. autoclass:: Attendances()

Attendee
#############
.. currentmodule:: models.event.Event.Attendances
.. autoclass:: Attendee()

Player
^^^^^^^^^^^^^^
.. currentmodule:: models.player
.. autoclass:: Player()

Patreon
+++++++++++++
.. currentmodule:: models.player.Player
.. autoclass:: Patreon()

Permissions
+++++++++++++
.. autoclass:: Permissions()

VTC
+++++++++++++
.. autoclass:: VTC()

Rules
^^^^^^^^^^^^^^
.. currentmodule:: models.rules
.. autoclass:: Rules()

Server
^^^^^^^^^^^^^^
.. currentmodule:: models.server
.. autoclass:: Server()

Version
^^^^^^^^^^^^^^
.. currentmodule:: models.version
.. autoclass:: Version()

ETS2MPChecksum
+++++++++++++
.. currentmodule:: models.version.Version
.. autoclass:: ETS2MPChecksum()

ATSMPChecksum
++++++++++++++++
.. autoclass:: ATSMPChecksum()

VTC
^^^^^^^^^^^^^^
.. currentmodule:: models.vtc
.. autoclass:: VTC()

Socials
+++++++++++++
.. currentmodule:: models.vtc.VTC
.. autoclass:: Socials()

Games
+++++++++++++
.. currentmodule:: models.vtc.VTC
.. autoclass:: Games()

VTCs
+++++++++++++
.. currentmodule:: models.vtc
.. autoclass:: VTCs()

VTC News Post
^^^^^^^^^^^^^^
.. currentmodule:: models.vtc
.. autoclass:: NewsPost()

VTC Role
^^^^^^^^^^^^^^
.. currentmodule:: models.vtc
.. autoclass:: Role()

VTC Member
^^^^^^^^^^^^^^
.. currentmodule:: models.vtc
.. autoclass:: Member()

Exceptions
--------------
Below are all the exceptions that the library may raise.

ConnectError
^^^^^^^^^^^^^^
.. autoexception:: truckersmp.exceptions.ConnectError

NotFoundError
^^^^^^^^^^^^^^
.. autoexception:: truckersmp.exceptions.NotFoundError

RateLimitError
^^^^^^^^^^^^^^
.. autoexception:: truckersmp.exceptions.RateLimitError

ServerError
^^^^^^^^^^^^^^
.. autoexception:: truckersmp.exceptions.ServerError

FormatError
^^^^^^^^^^^^^^
.. autoexception:: truckersmp.exceptions.FormatError
