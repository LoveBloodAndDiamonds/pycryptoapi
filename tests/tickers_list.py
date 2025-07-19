import asyncio

from pycryptoapi import ADAPTERS_MAPPER, CLIENTS_MAPPER
from pycryptoapi.enums import Exchange


async def main() -> None:
    for e in [Exchange.GATE]:
        client = await CLIENTS_MAPPER[e].create()

        tickers = await client.ticker()

        from pprint import pp

        # pp(tickers)

        tickers = ADAPTERS_MAPPER[e].ticker_24h(raw_data=tickers)

        pp(tickers)

        print(len(tickers))

        # Save tickers in .txt file for each exchange in a new line

        # with open(f"{e}_spot.txt", "w") as f:
        #     for ticker in tickers:
        #         f.write(f"{ticker}\n")


if __name__ == "__main__":
    asyncio.run(main())
