from datetime import datetime, timedelta
from typing import Union, Optional, Callable
from collections import namedtuple

from hashlib import sha1
from json import dumps
from asyncio import Event


def make_hashable(key, *args, **kwargs):
    """Make a variable value hashable, ready for caching"""
    if key is not None:
        # For lists and dictionaries, convert them into a hex string
        if type(key) is list:
            key = sha1(''.join(key).encode()).hexdigest()
        elif type(key) is dict:
            key = sha1(dumps(key, sort_keys=True).encode()).hexdigest()
    else:
        # If a cache key is not provided, use the args & kwargs of the function
        key = (args, tuple(kwargs.items()))
    return key


class Cache:
    class Object:
        """Represents an object in cache"""

        def __init__(self,
                     value: str,
                     added: datetime
                     ):
            self.value = value
            self.added = added

    class Info:
        """Represents the info about the cache"""

        def __init__(self,
                     name: Optional[str],
                     max_size: int,
                     time_to_live: timedelta,
                     minimise_size: bool
                     ):
            self.name = name
            self.hits = 0
            self.misses = 0
            self.expired_misses = 0
            self.size = 0
            self.max_size = max_size
            self.time_to_live = time_to_live
            self.minimise_size = minimise_size

        def add_hit(self):
            self.hits += 1

        def add_miss(self):
            self.misses += 1

        def add_expired_miss(self):
            self.expired_misses += 1

        def update_size(self, size: int):
            self.size = size

        def get(self):
            cache_info = namedtuple("CacheInfo", [
                "name", "hits", "misses", "expired_misses", "size", "max_size", "time_to_live", "minimise_size"
            ])
            return cache_info(
                self.name, self.hits, self.misses, self.expired_misses, self.size,
                self.max_size, self.time_to_live, self.minimise_size
            )

    def __init__(self,
                 name: Optional[str] = None,
                 max_size: Optional[int] = None,
                 time_to_live: Union[int, timedelta, None] = None,
                 minimise_size: bool = False  # No effect right now, requires async implementation
                 ):
        """
        :param name: The given name of the cache (simply for organisation, will be given with CacheInfo)
        :type max_size: Optional[str]
        :param max_size: The max size of the cache
        :type max_size: Optional[int]
        :param time_to_live: The live duration of each cache object (may not be deleted instantly or ever)
        :type time_to_live: Union[int, timedelta, None]
        :param minimise_size: Keep the cache size to a minimium by periodically removing expired items
        :type minimise_size: bool
        """
        self.name = name
        self.max_size = float('inf') if max_size is None else max_size
        if type(time_to_live) == int:
            time_to_live = timedelta(seconds=time_to_live)
        self.ttl = time_to_live
        self.minimise_size = minimise_size
        self.base = dict()
        self.info = self.Info(name, max_size, time_to_live, minimise_size)
        self.ongoing_executes = dict()

    def _get(self, key):
        """Get an object from the cache dictionary"""
        if key in self.base:
            self.info.add_hit()
            return self.base[key]
        self.info.add_miss()

    def _add(self, key, value):
        """Add an object via key-value to the cache dictonary"""
        self.base[key] = (self.Object(value, datetime.utcnow()))

    def _expired(self, obj):
        """Check if an object is expired"""
        if self.ttl: return (datetime.utcnow() - obj.added).total_seconds() >= self.ttl.total_seconds()

    def _del(self, key):
        """Delete an object from the cache dictionary"""
        if key in self.base: del self.base[key]

    def _del_old(self):
        """Delete the oldest cache entry (even if it hasn't expired)"""
        if len(self.base) > 0: del self.base[next(iter(self.base))]

    def _del_expired(self):
        """Delete expired items from the cache dictionary (potentially resource intensive)"""
        removed = 0
        for index, key, obj in enumerate(self.base.items()):
            if self._expired(obj):
                del self.base[key]
                removed += 1
        return removed

    def _get_execute_process_id(self, func: Callable, *args, **kwargs):
        process_id = (func.__name__, args, tuple(kwargs.items()))
        if process_id not in self.ongoing_executes:
            self.ongoing_executes[process_id] = Event()
            self.ongoing_executes[process_id].set()
        return process_id

    def add(self, key, value):
        """Add an object to the cache"""
        if len(self.base) >= self.max_size:
            self._del_old()
        self._add(key, value)

    def get(self, key):
        """Get an object from the cache"""
        obj = self._get(key)
        if not obj: return
        if self._expired(obj):
            self.info.add_expired_miss()
            del self.base[key]
            return
        return obj.value

    def get_info(self):
        """Get the info for this cache"""
        self.info.update_size(len(self.base))
        return self.info.get()

    def execute(self, func: Callable, key=None, *args, **kwargs):
        """
        Execute a function and save the result to this cache.
        When this is called again, if a result is found in cache, it is served instead of executing again.
        """
        key = make_hashable(key, *args, **kwargs)
        c = self.get(key)
        if c is not None:
            return c
        r = func(*args, **kwargs)
        self.add(key, r)
        return r

    async def execute_async(self, func: Callable, key=None, *args, **kwargs):
        """Async version of execute"""
        process_id = self._get_execute_process_id(func, *args, **kwargs)
        await self.ongoing_executes[process_id].wait()
        key = make_hashable(key, *args, **kwargs)
        c = self.get(key)
        if c is not None:
            return c

        self.ongoing_executes[process_id].clear()
        try:
            r = await func(*args, **kwargs)
        finally:
            self.ongoing_executes[process_id].set()

        self.add(key, r)
        return r
