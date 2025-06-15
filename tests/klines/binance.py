import asyncio

from pycryptoapi.binance import BinanceClient
from pycryptoapi.enums import Timeframe


async def main() -> None:
    client = await BinanceClient.create()

    r = await client.klines(symbol="BTCUSDT", timeframe=Timeframe.MIN_1)

    from pprint import pp
    pp(r)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
