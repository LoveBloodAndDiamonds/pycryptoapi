import asyncio

from pycryptoapi.binance import BinanceClient
from pycryptoapi.enums import Timeframe


async def main() -> None:
    client = await BinanceClient.create()

    r = await client.klines(symbol="BTCUSDT", interval=Timeframe.MIN_1)

    from datetime import datetime

    for el in r:
        print(datetime.fromtimestamp(el[0] / 1000))

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
