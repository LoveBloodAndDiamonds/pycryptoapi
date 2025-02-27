import asyncio

from pycryptoapi import MexcSocketManager, MexcAdapter
from pycryptoapi.enums import MarketType, Timeframe
from pycryptoapi.exceptions import AdapterException
from pycryptoapi.types import KlineDict


async def main():
    socket = MexcSocketManager.klines_socket(
        market_type=MarketType.SPOT,
        timeframe=Timeframe.MIN_1,
        tickers=["BTCUSDT", "ETHUSDT"],
        callback=callback
    )

    await socket.start()


async def callback(msg):
    try:
        # У каждой биржи есть свой адаптер, который приводит данные в единый формат.
        # Так, например, мы можем иметь одинаковый объект KlineDict для любой биржи.
        kline: KlineDict = MexcAdapter.kline_message(raw_msg=msg)
        print(kline)

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")

asyncio.run(main())
