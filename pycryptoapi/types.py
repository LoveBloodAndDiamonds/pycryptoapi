from typing import TypedDict, Optional


class Ticker24hItem(TypedDict):
    p: float  # price change percent
    v: float  # volume (USDT)


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
