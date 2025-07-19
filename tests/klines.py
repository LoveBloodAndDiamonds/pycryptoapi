import asyncio

from pycryptoapi import BybitClient, BybitAdapter
from pycryptoapi.enums import Timeframe
from loguru import logger


async def main() -> None:
    """Main entrypoint of the klines test"""
    client = await BybitClient.create()

    # r = await client.futures_klines(symbol="BTCUSDT", interval=Timeframe.MIN_5, limit=3)

    from pprint import pp
    pp(r)

    a = BybitAdapter.kline(raw_data=r)

    pp(a)

    await client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug("Keyboard interrupt")

