class WebsocketException(Exception):
    pass


class WrongMarketType(WebsocketException):
    def __init__(self, message="Incorrect market type provided"):
        super().__init__(message)


class WrongTimeframe(WebsocketException):
    def __init__(self, message="Incorrect timeframe provided"):
        super().__init__(message)


class WrongTickers(WebsocketException):
    def __init__(self, message="Incorrect tickers provided"):
        super().__init__(message)


class AdapterException(Exception):
    pass
