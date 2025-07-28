import asyncio

from pycryptoapi import XtClient
from pycryptoapi.enums import Exchange
from pycryptoapi.xt.adapter import XtAdapter


async def main() -> None:
    for e in [Exchange.XT]:
        client = await XtClient.create()

        tickers = await client.ticker()

        from pprint import pp

        # pp(tickers)
        #
        # return

        tickers = XtAdapter.futures_tickers(raw_data=tickers)

        pp(tickers)

        print(len(tickers))

        # Save tickers in .txt file for each exchange in a new line

        # with open(f"{e}_spot.txt", "w") as f:
        #     for ticker in tickers:
        #         f.write(f"{ticker}\n")

        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
