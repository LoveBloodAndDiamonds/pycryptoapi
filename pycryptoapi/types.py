from typing import TypedDict


class Ticker24hItem(TypedDict):
    p: float  # price change percent
    v: float  # volume (USDT)
