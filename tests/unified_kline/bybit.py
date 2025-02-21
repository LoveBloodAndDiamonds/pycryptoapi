import asyncio

# from pycryptoapi.binance import BinanceSocketManager
from pycryptoapi.bybit import BybitSocketManager


async def callback(msg):
    try:
        print(msg)
    except Exception as e:
        print("error", e, msg)


async def main():
    socket = BybitSocketManager.liquidations_socket(
        tickers=["BTCUSDT"],
        callback=callback
    )

    await socket.start()


asyncio.run(main())

'''

'''
