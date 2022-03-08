from datetime import datetime, timedelta
from typing import Union, Optional, List
from collections import deque


class Cache:
    class Object:
        def __init__(self,
                     key: str,
                     value: str,
                     added: datetime
                     ):
            self.key = key
            self.value = value
            self.added = added

    def __init__(self,
                 max_size: Optional[int] = None,
                 time_to_live: Union[int, timedelta, None] = None,
                 smart_max: bool = False,
                 minimise_size: bool = False
                 ):
        """
        :param max_size: The max size of the cache
        :type max_size: Optional[int]
        :param time_to_live: The live duration of each cache object (may not be deleted instantly or ever)
        :type time_to_live: Union[int, timedelta, None]
        :param smart_max: Delete expired items first when max size is reached (CAUTION: drastically reduces performance)
        :type smart_max: bool
        :param minimise_size: Keep the cache size to a minimium by removing expired items
        :type minimise_size: bool
        """
        self.max_size = float('inf') if max_size is None else max_size
        if type(time_to_live) == int:
            time_to_live = timedelta(seconds=time_to_live)
        self.ttl = time_to_live
        self.smart_max = smart_max
        self.minimise_size = minimise_size
        self.base = deque()

    async def _get(self, key):
        for obj in self.base:
            if obj.key == key:
                return obj

    async def _expired(self, obj):
        return (datetime.utcnow() - obj.added).total_seconds() >= self.ttl.total_seconds()

    async def _auto_del(self, limit: Optional[int] = 1, force_del: Optional[int] = 1):
        limit = float('inf') if limit is None else limit
        force_del = 0 if limit is None else force_del
        removed = 0
        for index, obj in enumerate(list(self.base)):
            if removed >= limit:
                return
            if await self._expired(obj):
                self.base.remove(obj)
                removed += 1
        if len(self.base) > 0:
            for _ in range(max(0, force_del - removed)):
                self.base.popleft()

    async def add(self, key, value):
        if len(self.base) >= self.max_size:
            if self.smart_max:
                await self._auto_del(limit=None if self.minimise_size else 1)
            else:
                self.base.popleft()
        self.base.append(self.Object(key, value, datetime.utcnow()))

    async def get(self, key):
        obj = await self._get(key)
        if self.minimise_size:
            await self._auto_del(limit=None)
        if not obj:
            return
        if await self._expired(obj):
            self.base.remove(obj)
            return
        return obj.value
