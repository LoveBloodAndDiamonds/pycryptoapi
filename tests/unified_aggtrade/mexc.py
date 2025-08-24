import asyncio

from pycryptoapi.exceptions import AdapterException

from pycryptoapi import SOCKETS_MAPPER, ADAPTERS_MAPPER, MexcAdapter
from pycryptoapi.enums import MarketType, Exchange
from pycryptoapi.fixes import init_mexc_perpetual_fix, mexc_perpetual_aggtrade_fix

exchange = Exchange.MEXC


async def callback(msg):
    try:
        # print(len(msg.publicAggreDeals.deals))
        # print(type(msg))
        # print(dict(msg))
        # print(msg.deals)
        # msg = mexc_perpetual_aggtrade_fix(msg)
        # print(msg)
        # print()

        k = MexcAdapter.aggtrades_message(raw_msg=msg)
        print(k)
        print()

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


async def main():
    await init_mexc_perpetual_fix()
    socket = SOCKETS_MAPPER[exchange].aggtrades_socket(
        market_type=MarketType.SPOT,
        # tickers=["BTCUSDT"],
        tickers=["BTCUSDT", "ETHUSDT"],
        callback=callback,
    )

    await socket.start()


asyncio.run(main())
