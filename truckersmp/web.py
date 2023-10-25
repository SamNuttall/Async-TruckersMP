import asyncio
import aiohttp

from truckersmp import exceptions
from typing import Optional
from aiolimiter import AsyncLimiter


async def get_request(
        url: str,
        logger,
        headers: dict = None,
        params: dict = None,
        timeout: int = 10,
        limiter: AsyncLimiter = None,
) -> Optional[dict]:
    """
    Makes a web get request (eg. to an API) for JSON.

    :param url: The endpoint of the get request
    :type url: str
    :param headers: HTTP headers to send with the request, defaults to None
    :type headers: dict, optional
    :param params: Parameters to pass with request, defaults to None
    :type params: dict, optional
    :param timeout: How many seconds to wait for a response before throwing a timeout error, defaults to 10.
    :type timeout: int, optional
    :return: JSON given by the API as a Python dictionary
    :rtype: Optional[dict]
    :param limiter: A limiter to abide by.
    :type limiter: :class:`aiolimiter.AsyncLimiter`, optional

    """

    # TEMP FIX - further research required
    user_agent = "Mozilla/5.0"
    if 'truckyapp' in url:
        if headers is None:
            headers = {'User-Agent': user_agent}  # Some APIs want a user-agent, otherwise will return 403
        else:
            headers['User-Agent'] = user_agent

    if limiter:
        await limiter.acquire()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params, timeout=timeout) as resp:
                logger.debug(f"GET Request: {url} = {resp.status}")
                if str(resp.status).startswith('2'):
                    return await resp.json()
                if resp.status == 429:
                    raise exceptions.RateLimitError()
                if resp.status == 404:
                    raise exceptions.NotFoundError()
                if str(resp.status).startswith('4') or str(resp.status).startswith('5'):
                    raise exceptions.ConnectError()
    except (aiohttp.ClientError, asyncio.TimeoutError, aiohttp.ServerTimeoutError):
        raise exceptions.ConnectError()