from typing import TypedDict, Optional, NamedTuple


class Ticker24hItem(TypedDict):
    p: float  # price change percent
    v: float  # volume (USDT)


class OpenInterestItem(NamedTuple):
    t: int  # time
    v: float  # value


class UnifiedKline(TypedDict):
    s: str  # symbol
    t: int  # open time
    o: float  # open price
    h: float  # high price
    l: float  # low price
    c: float  # close price
    v: float  # volume (USDT)
    i: str  # timeframe
    T: Optional[int]  # close time
    x: Optional[bool]  # is closed?
