import asyncio

from pycryptoapi import ADAPTERS_MAPPER, CLIENTS_MAPPER
from pycryptoapi.enums import Exchange


async def main() -> None:
    for e in Exchange:
        client = await CLIENTS_MAPPER[e].create()

        tickers = await client.ticker()

        tickers = ADAPTERS_MAPPER[e].tickers(raw_data=tickers)

        # Save tickers in .txt file for each exchange in a new line

        with open(f"{e}_spot.txt", "w") as f:
            for ticker in tickers:
                f.write(f"{ticker}\n")


if __name__ == "__main__":
    asyncio.run(main())
