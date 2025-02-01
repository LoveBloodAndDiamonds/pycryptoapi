import asyncio

from pycryptoapi.exceptions import AdapterException
# from pycryptoapi.binance import BinanceSocketManager
from pycryptoapi.okx import OkxSocketManager, OkxAdapter


async def callback(msg):
    try:
        k = OkxAdapter.kline_message(raw_msg=msg)
        for i in k:
            print(i)
    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = OkxSocketManager.klines_socket(
        # market_type=MarketType.FUTURES,
        timeframe="1m",
        tickers=["BTC-USDT"],
        callback=callback
    )

    await socket.start()


asyncio.run(main())

'''

'''
