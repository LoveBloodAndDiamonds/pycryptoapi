from typing import TypedDict, Optional, Union, List, Dict, TypeAlias, Literal

from .enums import Side

JsonLike: TypeAlias = Union[Dict, List]


class TickerDailyItem(TypedDict):
    p: float  # price change percent
    v: float  # volume (USDT)


class OpenInterestItem(TypedDict):
    t: int  # time
    v: float  # open interest (COIN)


TickerDailyDict: TypeAlias = Dict[str, TickerDailyItem]

OpenInterestDict: TypeAlias = Dict[str, OpenInterestItem]


class KlineDict(TypedDict):
    s: str  # symbol  # АЯЗ ИЗ БУДУЩЕГО, КОГДА ТЫ БУДЕШЬ ЭТО ДЕЛАТЬ - УБЕРИ ОТСЮДА ЭТОТ АТТРИБУТ, ПОТОМУ ЧТО ОН ТУТ ОЧЕВИДНО ЛИШНИЙ И НИКОГДА НЕ ПРИГОДИТСЯ
    t: int  # open time
    o: float  # open price
    h: float  # high price
    l: float  # low price
    c: float  # close price
    v: float  # volume (USDT)
    i: Optional[str]  # timeframe
    T: Optional[int]  # close time
    x: Optional[bool]  # is closed?


class AggTradeDict(TypedDict):
    t: int  # trade time
    s: str  # symbol
    S: Side | Literal["BUY", "SELL"]  # side
    p: float  # trade price
    v: float  # trade volume (Coins)


class LiquidationDict(TypedDict):
    t: int  # time
    s: str  # symbol
    S: Side | Literal["BUY", "SELL"]  # side
    v: float  # volume (Coins)
    p: float  # price
