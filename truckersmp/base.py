import asyncio
import logging

from aiolimiter import AsyncLimiter
from typing import Union, Optional, List, Callable
from datetime import timedelta, datetime
from .cache import Cache
from .endpoints import Endpoints
from .web import get_request
from .models.server import Server
from .models.player import Player
from .models.ban import Ban
from .models.event import Event, Events, EventsAttributes
from .models.vtc import VTC, VTCs, VTCsAttributes, NewsPost, Role, Member
from .models.version import Version
from .models.rules import Rules
from . import exceptions


async def execute(func: Callable, *args, **kwargs):
    """Execute a function and simplify any errors into ExecuteError and NotFoundError"""
    try:
        r = await func(*args, **kwargs)
    except exceptions.NotFoundError:
        raise exceptions.NotFoundError()
    except (exceptions.ConnectError, exceptions.FormatError, exceptions.RateLimitError):
        raise exceptions.ExecuteError()
    else:
        return r


async def wrapper(url, cache, timeout, limiter, logger, key=None, *args, **kwargs):
    """A wrapper to handle exceptions with cache. This will keep the rate-limit in check."""
    class CacheExceptionValues:
        ConnectError = "cache-instruction: to raise - ConnectError"
        FormatError = "cache-instruction: to raise - FormatError"
        NotFoundError = "cache-instruction: to raise - NotFoundError"

    try:
        r = await cache.execute_async(get_request, key, url, logger, timeout=timeout, limiter=limiter, *args, **kwargs)
    except exceptions.ConnectError:
        r = CacheExceptionValues.ConnectError
    except exceptions.FormatError:
        r = CacheExceptionValues.FormatError
    except exceptions.NotFoundError:
        r = CacheExceptionValues.NotFoundError
    else:
        if r == CacheExceptionValues.ConnectError:
            raise exceptions.ConnectError
        if r == CacheExceptionValues.FormatError:
            raise exceptions.FormatError
        if r == CacheExceptionValues.NotFoundError:
            raise exceptions.NotFoundError

        return r


class TruckersMP:
    """
    The main/base class to import when using the API wrapper. Configurable on initialisation by parameter passing.
    All endpoints return a value (mostly a class or list of classes) if the request is successful, None if something
    was not found and False if the request failed.

    :param loop: The asyncio loop to use. Tries to get if none provided.
    :type loop: :class:`asyncio.AbstractEventLoop`, optional
    :param limiter: Override the default limiter, defaults to 5 API requests/5 sec (60req/m).
    :type limiter: :class:`aiolimiter.AsyncLimiter`, optional
    :param logger: A custom logger to use, defaults to result of logging.getLogger().
    :type logger: :class:`logging.Logger`, optional
    :param log_freq: How frequently to log rate limit warnings, defaults to 60.
    :type log_freq: Union[int (as seconds), timedelta], optional
    :param min_queue_for_log: The minimum queue size required to start logging rate limits warnings.
        This will prevent warning logs for a small burst of requests, defaults to 10.
    :type min_queue_for_log: int, optional
    :param request_timeout: The number of seconds to wait for the API's response, defaults to 10.
    :type request_timeout: int, optional
    :param cache_time_to_live: The number of seconds to cache a for response before considering it expired, defaults
        to 60.
    :type cache_time_to_live: int, optional
    :param cache_max_size: The maximum number of items in the cache. Provide None for infinite size, defaults to 65536.
    :type cache_max_size: Optional[int], optional
    """

    def __init__(self,
                 loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
                 limiter: AsyncLimiter = AsyncLimiter(5, 5),
                 logger: logging.Logger = logging.getLogger(),
                 log_freq: Union[int, timedelta] = 60,
                 min_queue_for_log: int = 10,
                 request_timeout: int = 10,
                 cache_time_to_live: Optional[int] = 60,  # Seconds
                 cache_max_size: Optional[int] = 65536
                 ):
        self.loop = loop
        self.limiter = limiter
        self.req_per_sec = self.limiter.time_period / self.limiter.max_rate
        self.logger = logger
        if type(log_freq) == int:
            log_freq = timedelta(seconds=log_freq)
        self.log_freq = log_freq
        self.timeout = request_timeout
        self.cache = Cache(name="async-truckersmp", max_size=cache_max_size, time_to_live=cache_time_to_live)
        self.rate_limit = {
            'last_log': datetime.utcnow() - self.log_freq,
            'queue': 0,
            'min_queue_for_log': min_queue_for_log
        }

    async def get_player(self, player_id: int) -> Union[Player, bool, None]:
        """
        Get a specific TruckersMP player from the API using their player id

        :param player_id: TruckersMP Player ID
        :type player_id: int
        :return: :class:`Player <models.player.Player>`
        :rtype: Union[:class:`Player <models.player.Player>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.PLAYER_LOOKUP + str(player_id)
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        try:
            if resp['error']:
                if resp['descriptor'] == "Unable to find player with that ID.":  # TruckersMP doesn't raise a 404
                    raise exceptions.NotFoundError()
                raise exceptions.ConnectError()
            player = Player(resp['response'])
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        else:
            return player

    async def get_bans(self, player_id: int) -> Union[List[Ban], bool, None]:
        """
        Get a list of a TruckersMP player's bans.

        :param player_id: TruckersMP Player ID
        :type player_id: int
        :return: List of :class:`Ban <models.ban.Ban>`
        :rtype: Union[:class:`Ban <models.ban.Ban>`], bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.BANS_LOOKUP + str(player_id)
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        bans = list()
        try:
            if resp['error']:
                if resp['descriptor'] == "Invalid user ID":  # TruckersMP doesn't raise a 404
                    raise exceptions.NotFoundError()
                raise exceptions.ConnectError()
            for ban in resp['response']:
                bans.append(Ban(ban))
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return bans

    async def get_servers(self) -> Union[List[Server], bool, None]:
        """
        Get a list of TruckersMP servers

        :return: list of :class:`Server <models.server.Server>`
        :rtype: Union[List[:class:`Server <models.server.Server>`], bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.SERVERS
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        servers = list()
        try:
            for server in resp['response']:
                servers.append(Server(server))
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        else:
            return servers

    async def get_ingame_time(self) -> Union[int, bool, None]:
        """
        Get the ingame-time as an integer.

        :return: Ingame-time
        :rtype: Union[int, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.INGAME_TIME
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        try:
            game_time = resp['game_time']
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return game_time

    async def get_events(self) -> Union[Events, bool, None]:  # Rewritten
        """
        Get featured, todays and upcoming events.

        .. note::
            An event's confirmed_users and unsure_users will be None when making this call. Get a specific event
            via it's ID to get all confirmed and unsure users.

        :return: :class:`Events <models.event.Events>`
        :rtype: Union[:class:`Events <models.event.Events>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.EVENTS
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)

        event_types = (EventsAttributes.featured,
                       EventsAttributes.today,
                       EventsAttributes.now,
                       EventsAttributes.upcoming
                       )
        events_dict = {event_types[0]: [], event_types[1]: [], event_types[2]: [], event_types[3]: []}

        try:
            response = resp['response']
            for event_type in event_types:
                if event_type not in response:
                    continue
                for event in response[event_type]:
                    events_dict[event_type].append(Event(event))
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        else:
            return Events(events_dict)

    async def get_event(self, event_id: int) -> Union[Event, bool, None]:
        """
        Get a specific event

        :param event_id: An event ID
        :type event_id: int
        :return: :class:`Event <models.event.Event>`
        :rtype: Union[:class:`Event <models.event.Event>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.EVENT_LOOKUP + str(event_id)
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        if resp is None:
            raise exceptions.NotFoundError()
        try:
            event = Event(resp['response'])
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return event

    async def get_vtcs(self) -> Union[VTCs, bool, None]:
        """
        Get recent, featured and featured cover VTCs.

        :return: :class:`VTCs <models.vtc.VTCs>`
        :rtype: Union[:class:`VTCs <models.vtc.VTCs>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.VTCS
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        vtc_types = (VTCsAttributes.recent,
                     VTCsAttributes.featured,
                     VTCsAttributes.featured_cover
                     )
        vtcs_dict = {vtc_types[0]: [], vtc_types[1]: [], vtc_types[2]: []}
        try:
            for index, vtc_type in enumerate(resp['response'].values()):
                for vtc in vtc_type:
                    vtcs_dict[vtc_types[index]].append(VTC(vtc))
            vtcs = VTCs(vtcs_dict)
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return vtcs

    async def get_vtc(self, vtc_id: int) -> Union[VTC, bool, None]:
        """
        Get a specific VTC.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :return: :class:`VTC <models.vtc.VTC>`
        :rtype: Union[:class:`VTC <models.vtc.VTC>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.VTC_LOOKUP + str(vtc_id)
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        if resp is None:
            raise exceptions.NotFoundError()
        try:
            vtc = VTC(resp['response'])
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return vtc

    async def get_vtc_news(self, vtc_id: int) -> Union[List[NewsPost], bool, None]:
        """
        Get all news posts from a specific VTC.

        .. note::
            An news post's content (not content_summary) will be None when making this API call. Get a specific post
            via it's ID to get the full content.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :return: List of :class:`NewsPost <models.vtc.NewsPost>`
        :rtype: Union[List[:class:`NewsPost <models.vtc.NewsPost>`], bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.VTC_LOOKUP + str(vtc_id) + Endpoints.VTC_NEWS
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        posts = list()
        if resp is None:
            raise exceptions.NotFoundError()
        try:
            for news_post in resp['response']['news']:
                posts.append(NewsPost(news_post))
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return posts

    async def get_vtc_news_post(self, vtc_id: int, news_post_id: int
                                ) -> Union[NewsPost, bool, None]:
        """
        Get a specific news post from a specific VTC.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :param news_post_id: A news post's ID
        :type news_post_id: int
        :return: :class:`NewsPost <models.vtc.NewsPost>`
        :rtype: Union[:class:`NewsPost <models.vtc.NewsPost>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.VTC_LOOKUP + str(vtc_id) + Endpoints.VTC_NEWS + str(news_post_id)
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        if resp is None:
            raise exceptions.NotFoundError()
        try:
            post = NewsPost(resp['response'])
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return post

    async def get_vtc_roles(self, vtc_id: int) -> Union[List[Role], bool, None]:
        """
        Get all of a VTC's roles.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :return: List of :class:`Role <models.vtc.Role>`
        :rtype: Union[List[:class:`Role <models.vtc.Role>`], bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.VTC_LOOKUP + str(vtc_id) + Endpoints.VTC_ROLES
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        vtc_roles = list()
        if resp is None:
            raise exceptions.NotFoundError()
        try:
            for vtc_role in resp['response']['roles']:
                vtc_roles.append(Role(vtc_role))
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return vtc_roles

    async def get_vtc_role(self, vtc_id: int, role_id: int) -> Union[Role, bool, None]:
        """
        Get a specific role of a specific VTC.

        .. note::
            The info given by the TruckersMP API for VTC roles is the same, regardless of endpoint. Therefore,
            to reduce the number of API requests, this will make 1 call for all of a VTC's roles (or use cache) and
            search for the specified ID locally.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :param role_id: A VTC news post's ID
        :type role_id: int
        :return: :class:`Role <models.vtc.Role>`
        :rtype: Union[:class:`Role <models.vtc.Role>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        vtc_roles = await self.get_vtc_roles(vtc_id)
        for vtc_role in vtc_roles:
            if vtc_role.id == role_id:
                return vtc_role
        raise exceptions.NotFoundError()

    async def get_vtc_members(self, vtc_id: int) -> Union[List[Member], bool, None]:
        """
        Get all of a VTC's members.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :return: List of :class:`Member <models.vtc.Member>`
        :rtype: Union[List[:class:`Member <models.vtc.Member>`], bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.VTC_LOOKUP + str(vtc_id) + Endpoints.VTC_MEMBERS
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        vtc_members = list()
        if resp is None:
            raise exceptions.NotFoundError()
        try:
            for vtc_member in resp['response']['members']:
                vtc_members.append(Member(vtc_member))
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return vtc_members

    async def get_vtc_member(self, vtc_id: int, member_id: int) -> Union[Member, bool, None]:
        """
        Get a specific member that's within a specific VTC.

        .. note::
            The info given by the TruckersMP API for VTC members is the same, regardless of endpoint. Therefore,
            to reduce the number of API requests, this will make 1 call for all of a VTC's members (or use cache) and
            search for the specified ID locally.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :param member_id: A VTC's member ID
        :type member_id: int
        :return: :class:`Member <models.vtc.Member>`
        :rtype: Union[:class:`Member <models.vtc.Member>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        vtc_members = await self.get_vtc_members(vtc_id)
        for vtc_member in vtc_members:
            if vtc_member.id == member_id:
                return vtc_member
        raise exceptions.NotFoundError()

    async def get_vtc_events(self, vtc_id: int) -> Union[List[Event], bool, None]:
        """
        Get all of a VTC's events.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :return: List of :class:`Event <models.event.Event>`
        :rtype: Union[List[:class:`Event <models.event.Event>`], bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.VTC_LOOKUP + str(vtc_id) + Endpoints.VTC_EVENTS
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        events = list()
        if resp is None:
            raise exceptions.NotFoundError()
        try:
            for event in resp['response']:
                events.append(Event(event))
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return events

    async def get_vtc_event(self, vtc_id: int, event_id: int) -> Union[Event, bool, None]:
        """
        Get a specific VTC's event.

        .. note::
            An event's confirmed_users and unsure_users will be None when making this call. Get a specific event
            via it's ID to get all confirmed and unsure users.

        :param vtc_id: A VTC's ID
        :type vtc_id: int
        :param event_id: A VTC's event ID
        :type event_id: int
        :return: :class:`Event <models.event.Event>`
        :rtype: Union[:class:`Event <models.event.Event>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        url = Endpoints.VTC_LOOKUP + str(vtc_id) + Endpoints.VTC_EVENTS + str(event_id)
        resp = await wrapper(url, self.cache, self.timeout, self.limiter, self.logger)
        if resp is None:
            raise exceptions.NotFoundError()
        try:
            event = Event(resp['response'])
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return event

    async def get_version(self) -> Union[Version, bool, None]:
        """
        Get version information.

        :return: :class:`Version <models.version.Version>`
        :rtype: Union[:class:`Version <models.version.Version>`, bool, None]
        """
        resp = await wrapper(Endpoints.VERSION, self.cache, self.timeout, self.limiter, self.logger)
        try:
            version = Version(resp)
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return version

    async def get_rules(self) -> Union[Rules, bool, None]:
        """
        Get the latest TruckersMP rules.

        :return: :class:`Rules <models.rules.Rules>`
        :rtype: Union[:class:`Rules <models.rules.Rules>`, bool, None]
        """
        resp = await wrapper(Endpoints.RULES, self.cache, self.timeout, self.limiter, self.logger)
        try:
            rules = Rules(resp)
        except (KeyError, TypeError):
            raise exceptions.FormatError()
        return Rules(resp)
