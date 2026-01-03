import asyncio

from pycryptoapi import ADAPTERS_MAPPER, SOCKETS_MAPPER
from pycryptoapi.enums import Exchange, MarketType
from pycryptoapi.exceptions import AdapterException

exchange = Exchange.BINGX


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
        tickers=["BTC-USDT"],
        callback=callback,
    )

    await socket.start()


asyncio.run(main())
