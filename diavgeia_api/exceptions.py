class DiavgeiaError(Exception):
    """Base exception for the Diavgeia API."""


class DiavgeiaAPIError(DiavgeiaError):
    def __init__(self, status_code, message):
        super().__init__(f"API Error {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class DiavgeiaNetworkError(DiavgeiaError):
    """Network-related errors."""
