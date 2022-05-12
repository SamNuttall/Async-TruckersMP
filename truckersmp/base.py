import asyncio
import logging

from aiolimiter import AsyncLimiter
from typing import Union, Optional, List
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


class TruckersMP:
    """
    The main/base class to import when using the API wrapper. Configurable on initialisation by parameter passing.
    All endpoints return a value (mostly a class or list of classes) if the request is successful, None if something
    was not found and False if the request failed.

    :param loop: The asyncio loop to use. Tries to get if none provided.
    :type loop: :class:`asyncio.AbstractEventLoop`, optional
    :param limiter: Override the default limiter, defaults to 5 API requests/5 sec (60req/s).
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
    :param auto_handle_request_errors: When enabled, False (bool) will be returned when a request to an endpoint fails.
        Any future requests to the same endpoint will be locked/held for retry_time, defaults to True
    :type auto_handle_request_errors: bool, optional
    :param auto_handle_notfound_errors: When enabled, None will be returned when the API returns a not found error (404)
        . Future requests will not be locked, defaults to True
    :type auto_handle_notfound_errors: bool, optional
    :param auto_handle_ratelimit_errors: When enabled, False (bool) will be returned when the API returns a rate limit
        error (429). Any future requests to the same endpoint will be locked/held for retry_time. Under normal
        circumstances, the default limiter should stop this happening, defaults to False
    :type auto_handle_ratelimit_errors: bool, optional
    :param retry_time: Seconds to lock/hold further requests (per-endpoint) when the previous request raised an error
        , defaults to 20
    :type retry_time: int, optional
    """

    def __init__(self,
                 loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
                 limiter: AsyncLimiter = AsyncLimiter(5, 5),
                 logger: logging.Logger = logging.getLogger(),
                 log_freq: Union[int, timedelta] = 60,
                 min_queue_for_log: int = 10,
                 request_timeout: int = 10,
                 cache_time_to_live: Optional[int] = 60,  # Seconds
                 cache_max_size: Optional[int] = 65536,
                 auto_handle_request_errors: bool = True,
                 auto_handle_ratelimit_errors: bool = True,
                 auto_handle_notfound_errors: bool = False,
                 retry_time: int = 20  # Seconds
                 ):
        self.loop = loop
        self.limiter = limiter
        self.req_per_sec = self.limiter.time_period / self.limiter.max_rate
        self.logger = logger
        if type(log_freq) == int:
            log_freq = timedelta(seconds=log_freq)
        self.log_freq = log_freq
        self.timeout = request_timeout
        self.cache = Cache(cache_max_size, cache_time_to_live, smart_max=True)
        self.auto_handle_request_errors = auto_handle_request_errors
        self.auto_handle_ratelimit_errors = auto_handle_ratelimit_errors
        self.auto_handle_notfound_errors = auto_handle_notfound_errors
        self.retry_time = retry_time
        self.ongoing_requests = dict()

        self.rate_limit = {
            'last_log': datetime.utcnow() - self.log_freq,
            'queue': 0,
            'min_queue_for_log': min_queue_for_log
        }

    async def _make_request(self, url) -> Optional[dict]:
        """
        Make a get request that adheres to the class's configuration (such as rate limit, logging).

        :return: The JSON response given by the API as a Python dictionary
        :rtype: Optional[dict]
        """
        if not self.limiter.has_capacity():
            sec_since_last_log = (datetime.utcnow() - self.rate_limit['last_log']).total_seconds()
            if sec_since_last_log > self.log_freq.total_seconds():
                if self.rate_limit['min_queue_for_log'] <= self.rate_limit['queue']:
                    queue_len = self.rate_limit['queue'] + 1
                    self.logger.warning("A user-defined rate limit has been reached! "
                                        f"{queue_len} request(s) in queue")
                    self.rate_limit['last_log'] = datetime.utcnow()
        self.rate_limit['queue'] += 1
        async with self.limiter:
            try:
                return await get_request(url, timeout=self.timeout)
            finally:
                self.rate_limit['queue'] -= 1

    async def _process_request(self, url) -> Union[dict, bool, None]:
        """
        Process a request by checking if it's in cache before making an API request.
        Will hold further requests (per-endpoint) if an existing request is in progress, then check cache.

        .. _base__process_request:

        :return: The JSON response given by the API as a Python dictionary
        :rtype: Optional[dict]
        :raises truckersmp.exceptions.NotFoundError: If the resource (eg. player) is not found and
                auto_handle_notfound_errors is False
        :raises truckersmp.exceptions.ConnectError: If something went wrong while making an API request and
                auto_handle_request_errors is False
        :raises truckersmp.exceptions.RateLimitError: If a rate limit error (429) is returned by the API and
                auto_handle_ratelimit_errors is False
        """
        key = (url,)

        # Create event lock if not exist
        if key not in self.ongoing_requests:
            self.ongoing_requests[key] = asyncio.Event()
            self.ongoing_requests[key].set()

        # Wait if a call on the same endpoint is in progress
        await self.ongoing_requests[key].wait()

        # Get from cache, continue if expired or nothing
        cache = await self.cache.get(key)
        if cache:
            return cache

        # We're about to make an API call, lock further requests on this endpoint
        self.ongoing_requests[key].clear()

        async def handle_error(should_raise, reason, retry_time):
            if should_raise:
                raise
            await hold_lock(f"Failed to make a request due to {reason}; automatically handling... "
                            f"Future requests on this endpoint are locked for {retry_time} seconds.",
                            retry_time)

        async def hold_lock(warn_msg, hold_time):
            self.logger.warning(warn_msg)
            await asyncio.sleep(hold_time)

        try:
            resp = await self._make_request(url)
        except exceptions.ConnectError:
            await handle_error(self.auto_handle_request_errors, "a connection error", self.retry_time)
        except exceptions.RateLimitError:
            await handle_error(self.auto_handle_ratelimit_errors, "a rate-limit error", self.retry_time)
        except exceptions.NotFoundError:
            if self.auto_handle_request_errors:
                return None
            raise
        else:
            await self.cache.add(key, resp if resp is not None else "None")
            return resp
        finally:
            self.ongoing_requests[key].set()

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
        resp = await self._process_request(url)
        return Player(resp['response'])

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
        resp = await self._process_request(url)
        bans = list()
        for ban in resp['response']:
            bans.append(Ban(ban))
        return bans

    async def get_servers(self) -> Union[List[Server], bool, None]:
        """
        Get a list of TruckersMP servers

        :return: list of :class:`Server <models.server.Server>`
        :rtype: Union[List[:class:`Server <models.server.Server>`], bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        resp = await self._process_request(Endpoints.SERVERS)
        servers = list()
        for server in resp['response']:
            servers.append(Server(server))
        return servers

    async def get_ingame_time(self) -> Union[int, bool, None]:
        """
        Get the ingame-time as an integer.

        :return: Ingame-time
        :rtype: Union[int, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        resp = await self._process_request(Endpoints.INGAME_TIME)
        return resp['game_time']

    async def get_events(self) -> Union[Events, bool, None]:
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
        resp = await self._process_request(Endpoints.EVENTS)
        event_types = (EventsAttributes.featured, EventsAttributes.today, EventsAttributes.upcoming)
        events_dict = {event_types[0]: [], event_types[1]: [], event_types[2]: []}
        for index, event_type in enumerate(resp['response'].values()):
            for event in event_type:
                events_dict[event_types[index]].append(Event(event))
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
        resp = await self._process_request(url)
        return Event(resp['response'])

    async def get_vtcs(self) -> Union[VTCs, bool, None]:
        """
        Get recent, featured and featured cover VTCs.

        :return: :class:`VTCs <models.vtc.VTCs>`
        :rtype: Union[:class:`VTCs <models.vtc.VTCs>`, bool, None]
        :raises: Refer to :mod:`_process_request() <truckersmp.base.TruckersMP._process_request>` as these errors
            will be passed through
        """
        resp = await self._process_request(Endpoints.VTCS)
        vtc_types = (VTCsAttributes.recent, VTCsAttributes.featured, VTCsAttributes.featured_cover)
        vtcs_dict = {vtc_types[0]: [], vtc_types[1]: [], vtc_types[2]: []}
        for index, vtc_type in enumerate(resp['response'].values()):
            for vtc in vtc_type:
                vtcs_dict[vtc_types[index]].append(VTC(vtc))
        return VTCs(vtcs_dict)

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
        try:
            resp = await self._process_request(url)
        except exceptions.NotFoundError:
            return False
        return VTC(resp['response'])

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
        resp = await self._process_request(url)
        posts = list()
        for news_post in resp['response']['news']:
            posts.append(NewsPost(news_post))
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
        resp = await self._process_request(url)
        return NewsPost(resp['response'])

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
        resp = await self._process_request(url)
        vtc_roles = list()
        for vtc_role in resp['response']['roles']:
            vtc_roles.append(Role(vtc_role))
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
        resp = await self._process_request(url)
        vtc_members = list()
        for vtc_member in resp['response']['members']:
            vtc_members.append(Member(vtc_member))
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
        resp = await self._process_request(url)
        events = list()
        for event in resp['response']:
            events.append(Event(event))
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
        resp = await self._process_request(url)
        return Event(resp['response'])

    async def get_version(self) -> Union[Version, bool, None]:
        """
        Get version information.

        :return: :class:`Version <models.version.Version>`
        :rtype: Union[:class:`Version <models.version.Version>`, bool, None]
        """
        resp = await self._process_request(Endpoints.VERSION)
        return Version(resp)

    async def get_rules(self) -> Union[Rules, bool, None]:
        """
        Get the latest TruckersMP rules.

        :return: :class:`Rules <models.rules.Rules>`
        :rtype: Union[:class:`Rules <models.rules.Rules>`, bool, None]
        """
        resp = await self._process_request(Endpoints.RULES)
        return Rules(resp)
