import asyncio

from pycryptoapi.exceptionsimport AdapterException

from pycryptoapi import SOCKETS_MAPPER, ADAPTERS_MAPPER
from pycryptoapi.enums import MarketType, Exchange

exchange = Exchange.BITGET


async def callback(msg):
    try:
        print(msg)
        k = ADAPTERS_MAPPER[exchange].aggtrades_message(raw_msg=msg)
        print(k)
        print()

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = SOCKETS_MAPPER[exchange].aggtrades_socket(
        market_type=MarketType.FUTURES,
        # tickers=["BTCUSDT"],
        tickers=["BTCUSDT", "ETHUSDT"],
        callback=callback,
    )

    await socket.start()


asyncio.run(main())
