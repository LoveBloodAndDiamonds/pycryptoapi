import asyncio

from pycryptoapi import GateClient, GateAdapter
from pycryptoapi.enums import Exchange


async def main() -> None:
    client = await GateClient.create()

    tickers = await client.futures_ticker()

    from pprint import pp

    pp(tickers)


    tickers = GateAdapter.futures_last_price(raw_data=tickers)

    pp(tickers)


    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
