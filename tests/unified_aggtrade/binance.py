import asyncio

from pycryptoapi import SOCKETS_MAPPER, ADAPTERS_MAPPER
from pycryptoapi.enums import MarketType, Exchange
from pycryptoapi.exceptions import AdapterException

exchange = Exchange.BINANCE


async def callback(msg):
    try:
        k = ADAPTERS_MAPPER[exchange].aggtrades_message(raw_msg=msg)
        print(k)

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = SOCKETS_MAPPER[exchange].aggtrades_socket(
        market_type=MarketType.SPOT,
        # tickers=["BTCUSDT"],
        tickers=["BTCUSDT"],
        callback=callback,
    )

    await socket.start()


asyncio.run(main())
