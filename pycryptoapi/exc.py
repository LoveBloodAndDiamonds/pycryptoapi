from typing import Optional


class PyCryptoAPIException(Exception):
    pass


class MarketException(PyCryptoAPIException):

    def __init__(self, message="Incorrect market type provided"):
        super().__init__(message)


class TimeframeException(PyCryptoAPIException):

    def __init__(self, message="Incorrect timeframe provided"):
        super().__init__(message)


class TickersException(PyCryptoAPIException):

    def __init__(self, message="Incorrect tickers provided"):
        super().__init__(message)


class AdapterException(PyCryptoAPIException):
    pass


class APIException(PyCryptoAPIException):

    def __init__(self, code: int, message: Optional[str] = "API Error"):
        super().__init__(message)
        self.code = code

    @property
    def is_rate_limit_exception(self) -> bool:
        return self.code == 429


class QueueOverflowException(PyCryptoAPIException):

    def __init__(self, message: str = "Queue overflowed...") -> None:
        super().__init__(message)
