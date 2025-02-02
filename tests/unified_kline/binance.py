import asyncio

from pycryptoapi.binance import BinanceSocketManager, BinanceAdapter
from pycryptoapi.exceptions import AdapterException
from pycryptoapi.enums import MarketType


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
        timeframe="1m",
        tickers=["BTCUSDT"],
        callback=callback
    )

    await socket.start()


asyncio.run(main())


'''

'''
