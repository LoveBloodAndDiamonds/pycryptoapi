import asyncio

# from pycryptoapi.binance import BinanceSocketManager
from pycryptoapi.bybit import BybitSocketManager, BybitAdapter


async def callback(msg):
    try:
        liq = BybitAdapter.liquidation_message(raw_msg=msg)
        print(liq)
    except Exception as e:
        print("error", e)


async def main():
    socket = BybitSocketManager.liquidations_socket(
        tickers=["BTCUSDT", "ETHUSDT", "XRPUSDT", "TRUMPUSDT", "SOLUSDT"],
        callback=callback,
        no_message_reconnect_timeout=120,
    )

    await socket.start()


asyncio.run(main())

'''

'''
