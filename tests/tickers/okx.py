import asyncio

from aiohttp import ClientSession

from pycryptoapi.okx import OkxClient, OkxAdapter


async def test_okx_tickers(session: ClientSession):
    client = OkxClient(session)
    raw_data = await client.ticker()
    tickers = OkxAdapter.tickers(raw_data)
    print("OKX tickers:", tickers)
    print("Total OKX tickers:", len(tickers))


async def test_okx_futures_tickers(session: ClientSession):
    client = OkxClient(session)
    raw_data = await client.futures_ticker()
    futures_tickers = OkxAdapter.futures_tickers(raw_data)
    print("OKX futures tickers:", futures_tickers)
    print("Total OKX futures tickers:", len(futures_tickers))


async def test_okx_ticker_24h(session: ClientSession):
    client = OkxClient(session)
    raw_data = await client.ticker()
    ticker_24h = OkxAdapter.ticker_24h(raw_data)
    print("OKX 24h ticker:", ticker_24h)
    print("Total OKX 24h tickers:", len(ticker_24h))


async def test_okx_futures_ticker_24h(session: ClientSession):
    client = OkxClient(session)
    raw_data = await client.futures_ticker()
    futures_ticker_24h = OkxAdapter.futures_ticker_24h(raw_data)
    print("OKX 24h futures ticker:", futures_ticker_24h)
    print("Total OKX 24h futures tickers:", len(futures_ticker_24h))


# To run all the tests for OKX
async def test_okx(session: ClientSession):
    # await test_okx_tickers(session)
    # await test_okx_futures_tickers(session)
    # await test_okx_ticker_24h(session)
    await test_okx_futures_ticker_24h(session)


# Running the tests for OKX
async def main():
    async with ClientSession() as session:
        await test_okx(session)


if __name__ == "__main__":
    asyncio.run(main())
