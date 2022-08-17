from datetime import datetime, timedelta
from typing import Union, Optional
from collections import namedtuple


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
                     max_size: int,
                     time_to_live: timedelta,
                     minimise_size: bool
                     ):
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
                "hits", "misses", "expired_misses", "size", "max_size", "time_to_live", "minimise_size"
            ])
            return cache_info(
                self.hits, self.misses, self.expired_misses, self.size,
                self.max_size, self.time_to_live, self.minimise_size
            )

    def __init__(self,
                 max_size: Optional[int] = None,
                 time_to_live: Union[int, timedelta, None] = None,
                 minimise_size: bool = False  # No effect right now, requires async implementation
                 ):
        """
        :param max_size: The max size of the cache
        :type max_size: Optional[int]
        :param time_to_live: The live duration of each cache object (may not be deleted instantly or ever)
        :type time_to_live: Union[int, timedelta, None]
        :param minimise_size: Keep the cache size to a minimium by periodically removing expired items
        :type minimise_size: bool
        """
        self.max_size = float('inf') if max_size is None else max_size
        if type(time_to_live) == int:
            time_to_live = timedelta(seconds=time_to_live)
        self.ttl = time_to_live
        self.minimise_size = minimise_size
        self.base = dict()
        self.info = self.Info(max_size, time_to_live, minimise_size)

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