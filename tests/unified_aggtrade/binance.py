import asyncio

from pycryptoapi import SOCKETS_MAPPER, ADAPTERS_MAPPER
from pycryptoapi.enums import MarketType, Exchange
from pycryptoapi.exceptions import AdapterException

exchange = Exchange.OKX
mtype = MarketType.FUTURES


async def callback(msg):
    try:
        # print(exchange, msg)
        k = ADAPTERS_MAPPER[exchange].aggtrades_message(raw_msg=msg)
        print(k)

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = SOCKETS_MAPPER[exchange].aggtrades_socket(
        market_type=mtype,
        tickers=["BTC-USDT-SWAP"],
        callback=callback,
    )

    await socket.start()


asyncio.run(main())
