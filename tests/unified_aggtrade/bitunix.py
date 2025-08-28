import asyncio

from pycryptoapi.bitunix import BitunixSocketManager, BitunixAdapter
from pycryptoapi.enums import MarketType, Exchange
from datetime import datetime


async def callback(msg):
    print(msg)

    a = BitunixAdapter.aggtrades_message(msg)

    print(a)


async def main():
    socket = BitunixSocketManager.aggtrades_socket(
        market_type=MarketType.FUTURES,
        tickers=["BTCUSDT", "ETHUSDT"],
        callback=callback,
    )

    await socket.start()


asyncio.run(main())
