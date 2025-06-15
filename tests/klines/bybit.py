import asyncio

from pycryptoapi.bybit import BybitClient
from pycryptoapi.enums import Timeframe


async def main() -> None:
    client = await BybitClient.create()

    r = await client.futures_klines(symbol="BTCUSDT", interval=Timeframe.MIN_1)

    from pprint import pp
    pp(r)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
