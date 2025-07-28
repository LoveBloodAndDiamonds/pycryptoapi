# import asyncio
#
# from pycryptoapi import SOCKETS_MAPPER, ADAPTERS_MAPPER
# from pycryptoapi.enums import Exchange, MarketType
# from pycryptoapi.exceptions import AdapterException
# from pycryptoapi.types import AggTradeDict
#
# exchange = Exchange.XT
#
# # class AggTradeDict(TypedDict):
# #     t: int  # trade time
# #     s: str  # symbol
# #     S: Side | Literal["BUY", "SELL"]  # side
# #     p: float  # trade price
# #     v: float  # trade volume (Coins
#
#
# async def callback(msg):
#     try:
#         aggtrades: list[AggTradeDict] = ADAPTERS_MAPPER[exchange].aggtrades_message(raw_msg=msg)
#     except AdapterException as e:
#         print(f"Can not adapt message ({e}): {msg}")
#
#
# async def main():
#     socket = SOCKETS_MAPPER[exchange].aggtrades_socket(
#         tickers=["btc_usdt"],
#         market_type=MarketType.FUTURES,
#         callback=callback,
#     )
#
#     await socket.start()
#
#
# asyncio.run(main())


import asyncio
import time
from collections import defaultdict
from pycryptoapi import SOCKETS_MAPPER, ADAPTERS_MAPPER
from pycryptoapi.enums import Exchange, MarketType
from pycryptoapi.exceptions import AdapterException
from pycryptoapi.types import AggTradeDict
from pycryptoapi.fixes import init_fixes, xt_perpetual_aggtrade_fix

exchange = Exchange.XT

CANDLE_INTERVAL = 60  # 1 минута

# Хранилище текущей свечи по тикеру
candles = defaultdict(lambda: {
    "open": None,
    "high": float("-inf"),
    "low": float("inf"),
    "close": None,
    "volume": 0.0,
    "start_time": None
})


def get_candle_start(ts: int) -> int:
    """Возвращает начало минуты (timestamp, кратный 60)."""
    return ts - (ts % CANDLE_INTERVAL)


last_start_time = 0


async def callback(msg):
    global last_start_time
    msg = xt_perpetual_aggtrade_fix(msg)
    try:
        aggtrades: list[AggTradeDict] = ADAPTERS_MAPPER[exchange].aggtrades_message(raw_msg=msg)
    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")
        return

    print(aggtrades)

    return

    now = int(time.time())
    current_start = get_candle_start(now)

    for trade in aggtrades:
        ticker = trade["s"]
        price = trade["p"]
        volume = trade["v"]
        data = candles[ticker]

        if last_start_time != current_start:  # Обновляем время и печатаем прошлую свечку
            last_start_time = current_start
            from pprint import pp
            print(time.ctime())
            pp(candles[ticker])
            print()
            candles[ticker] = {
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": volume,
                "start_time": current_start
            }

        else:
            # Обновляем текущую свечу
            data["high"] = max(data["high"], price)
            data["low"] = min(data["low"], price)
            data["close"] = price
            data["volume"] += volume


async def main():
    await init_fixes(Exchange.XT, MarketType.FUTURES)
    socket = SOCKETS_MAPPER[exchange].aggtrades_socket(
        tickers=["btc_usdt", "eth_usdt"],
        market_type=MarketType.SPOT,
        callback=callback,
    )

    await asyncio.gather(socket.start())


if __name__ == "__main__":
    asyncio.run(main())
