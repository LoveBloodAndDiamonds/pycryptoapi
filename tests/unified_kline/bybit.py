import asyncio

# from pycryptoapi.binance import BinanceSocketManager
from pycryptoapi.bybit import BybitSocketManager, BybitAdapter
from pycryptoapi.enums import MarketType
from pycryptoapi.exceptions import AdapterException


async def callback(msg):
    try:
        k = BybitAdapter.kline_message(raw_msg=msg)
        print(k)
    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = BybitSocketManager.klines_socket(
        market_type=MarketType.SPOT,
        timeframe="1",
        tickers=["BTCUSDT"],
        callback=callback
    )

    await socket.start()


asyncio.run(main())

'''

'''
