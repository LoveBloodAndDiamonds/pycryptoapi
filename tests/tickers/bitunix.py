import asyncio

from pycryptoapi.bitunix import BitunixClient, BitunixAdapter


async def main() -> None:
    client = await BitunixClient.create()

    tickers = await client.futures_ticker()

    tickers_list = BitunixAdapter.futures_tickers(tickers)

    tickers_24 = BitunixAdapter.futures_ticker_24h(tickers)

    from pprint import pp

    pp(tickers_24)

    pp(tickers_24["BTCUSDT"])

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
