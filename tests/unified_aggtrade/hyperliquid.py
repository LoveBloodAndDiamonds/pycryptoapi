import asyncio

from pycryptoapi.enums import MarketType
from pycryptoapi.hyperliquid import HyperliquidSocketManager, HyperliquidAdapter


async def callback(msg):
    r = HyperliquidAdapter.aggtrades_message(raw_msg=msg)
    for i in r:
        print(i)


async def main():
    socket = HyperliquidSocketManager.aggtrades_socket(
        market_type=MarketType.FUTURES,
        tickers=["UDZUSDC"],
        callback=callback,
    )
    await socket.start()


if __name__ == '__main__':
    asyncio.run(main())

