import asyncio

from pycryptoapi.hyperliquid import HyperliquidClient, HyperliquidAdapter


async def main() -> None:
    client = await HyperliquidClient.create()

    tickers = await client.ticker()

    from pprint import pp

    pp(tickers["tokens"])

    pp(tickers.keys())

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
