import asyncio

from pycryptoapi import BybitClient, BybitAdapter
from pycryptoapi.enums import Timeframe


async def main() -> None:
    client = await BybitClient.create()

    r = await client.futures_klines(symbol="BTCUSDT", interval=Timeframe.MIN_5, limit=3)

    from pprint import pp
    pp(r)

    a = BybitAdapter.kline(raw_data=r)

    pp(a)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
