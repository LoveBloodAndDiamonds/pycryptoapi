import asyncio

from pycryptoapi.binance import BinanceSocketManager, BinanceAdapter
from pycryptoapi.enums import MarketType, Timeframe
from pycryptoapi.exc import AdapterException


async def callback(msg):
    try:
        print(msg)
        k = BinanceAdapter.kline_message(raw_msg=msg)
        print(k)

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = BinanceSocketManager.klines_socket(
        market_type=MarketType.SPOT,
        timeframe=Timeframe.MIN_1,
        tickers=["BTCUSDT", "ETHUSDT"],
        callback=callback
    )

    await socket.start()


asyncio.run(main())


'''

'''
