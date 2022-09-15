class Error(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return super().__str__()


class ConnectError(Error):
    """
    Raised when an error occurs during an API request. It's likely a temporary problem with your internet or the API.
    """
    def __init__(self):
        self.message = "An error occurred while connecting to the API/server. This may be a temporary problem."
        super().__init__()

    def __str__(self) -> str:
        return self.message


class NotFoundError(Error):
    """Raised when a resource at an endpoint is not found such as providing a player ID that is not registered."""
    def __init__(self):
        self.message = "The specified resource cannot be found. Have you specified the correct parameters?"
        super().__init__()

    def __str__(self) -> str:
        return self.message


class RateLimitError(Error):
    """
    Raised when the API returns a 429 error.
    This should never happen in normal circumstances when using the default limiter.
    """
    def __init__(self):
        self.message = "The API sent a rate limit error. Reduce the number of requests being made. " \
                       "Have you modified the default limiter?"
        super().__init__()

    def __str__(self) -> str:
        return self.message


class FormatError(Error):
    """Raised when the API returns JSON that isn't in the format that's expected (eg. missing a key)"""
    def __init__(self):
        self.message = "The response was not provided in the correct format"
        super().__init__()

    def __str__(self) -> str:
        return self.message


class ExecuteError(Error):
    """Raised when the execute() function raises a different error. See execute function docs for more info."""
    def __init__(self):
        self.message = "The execute function ran a function because of a different error"
        super().__init__()

    def __str__(self) -> str:
        return self.message
