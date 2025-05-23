import asyncio

from pycryptoapi import MexcSocketManager, MexcAdapter
from pycryptoapi.enums import MarketType, Timeframe
from pycryptoapi.exceptions import AdapterException
from pycryptoapi.types import KlineDict
from pycryptoapi.fixes import init_mexc_perpetual_fix, mexc_perpetual_aggtrade_fix


async def main():
    await init_mexc_perpetual_fix()

    socket = MexcSocketManager.klines_socket(
        market_type=MarketType.FUTURES,
        timeframe=Timeframe.MIN_1,
        tickers=["BTCUSDT", "ETHUSDT"],
        callback=callback
    )

    await socket.start()


async def callback(msg):
    try:
        print(msg)

        msg = mexc_perpetual_aggtrade_fix(msg)

        print(msg)
        print()

        # У каждой биржи есть свой адаптер, который приводит данные в единый формат.
        # Так, например, мы можем иметь одинаковый объект KlineDict для любой биржи.
        # kline: list[KlineDict] = MexcAdapter.kline_message(raw_msg=msg)
        # print(kline)

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")

asyncio.run(main())
