import asyncio

from pycryptoapi import SOCKETS_MAPPER, ADAPTERS_MAPPER
from pycryptoapi.enums import Exchange, MarketType
from pycryptoapi.exceptions import AdapterException

exchange = Exchange.GATE


async def callback(msg):
    print(msg)
    try:
        k = ADAPTERS_MAPPER[exchange].aggtrades_message(raw_msg=msg)
        print(k)
        print()
    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = SOCKETS_MAPPER[exchange].aggtrades_socket(
        tickers=["BTCUSDT", "ETHUSDT"],
        market_type=MarketType.FUTURES,
        # tickers=["BTC-USDT-SWAP"],create_time_ms
        callback=callback,
    )

    await socket.start()


asyncio.run(main())
