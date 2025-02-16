import asyncio

from pycryptoapi.binance import BinanceSocketManager, BinanceAdapter, BinanceClient
from pycryptoapi.enums import MarketType
from pycryptoapi.exc import AdapterException


async def callback(msg):
    try:
        # import time
        # time.sleep(2)
        # await asyncio.sleep(2)
        # for i in range(1, 100000):
        await asyncio.sleep(0.05)
        k = BinanceAdapter.aggtrades_message(raw_msg=msg)
        # print(k)

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    # AbstractWebsocket.set_debug_queue_size(True)

    client = await BinanceClient.create()

    tickers = await client.futures_ticker()

    tickers = BinanceAdapter.futures_tickers(raw_data=tickers)

    tickers_chunk = [tickers[i: i + 40] for i in range(0, len(tickers), 40)]

    tasks = []
    for chunk in tickers_chunk:
        tasks.append(BinanceSocketManager.aggtrades_socket(
            market_type=MarketType.SPOT,
            tickers=chunk,
            callback=callback,
        ).start())

    await asyncio.gather(*tasks)

asyncio.run(main())


'''

'''
