import asyncio

from pycryptoapi.kcex import KcexClient, KcexAdapter


async def main() -> None:
    client = await KcexClient.create()

    tickers = await client.futures_ticker()

    from pprint import pp

    # pp(tickers)

    tickers_list = KcexAdapter.futures_tickers(raw_data=tickers)

    print(tickers_list)
    print(len(tickers_list))

    tickers24 = KcexAdapter.futures_ticker_24h(tickers)

    pp(tickers24)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
