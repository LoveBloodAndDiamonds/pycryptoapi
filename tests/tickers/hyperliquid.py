import asyncio

from pycryptoapi.hyperliquid import HyperliquidClient, HyperliquidAdapter


async def main() -> None:
    adapter = HyperliquidAdapter()
    client = await HyperliquidClient.create()

    raw_data = await client.futures_last_price()

    print(raw_data)

    a = adapter.futures_last_price(raw_data)

    from pprint import pp

    pp(a)

    # tickers24 = adapter.futures_ticker_24h(raw_data)

    # pp(tickers24)

    # open_interest = adapter.futures_tickers(raw_data)

    # pp(open_interest)

    # print(len(open_interest))

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
