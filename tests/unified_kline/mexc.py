import asyncio

from pycryptoapi.exceptions import AdapterException
# from pycryptoapi.binance import BinanceSocketManager
from pycryptoapi.mexc import MexcSocketManager, MexcAdapter
from pycryptoapi.enums import MarketType


async def callback(msg):
    try:
        k = MexcAdapter.kline_message(raw_msg=msg)
        print(k)
    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = MexcSocketManager.klines_socket(
        market_type=MarketType.FUTURES,
        timeframe="Min1",
        tickers=["BTCUSDT"],
        callback=callback
    )

    await socket.start()


asyncio.run(main())


'''

'''
