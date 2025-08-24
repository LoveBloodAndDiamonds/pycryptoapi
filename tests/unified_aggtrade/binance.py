import asyncio

from pycryptoapi import SOCKETS_MAPPER, ADAPTERS_MAPPER
from pycryptoapi.enums import MarketType, Exchange
from pycryptoapi.exceptions import AdapterException
from datetime import datetime

exchange = Exchange.BINANCE
mtype = MarketType.SPOT


async def callback(msg):
    t = msg["T"]
    ts = t / 1000
    dt = datetime.fromtimestamp(ts)
    print(dt, ": ", msg)
    # try:
    #     # print(exchange, msg)
    #     k = ADAPTERS_MAPPER[exchange].aggtrades_message(raw_msg=msg)
    #     print(k)
    #
    # except AdapterException as e:
    #     print(f"Can not adapt message ({e}): {msg}")


async def main():
    socket = SOCKETS_MAPPER[exchange].aggtrades_socket(
        market_type=mtype,
        tickers=["XRPUSDT"],
        callback=callback,
    )

    await socket.start()


asyncio.run(main())
