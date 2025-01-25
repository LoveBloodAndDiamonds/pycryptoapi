import asyncio

from aiohttp import ClientSession

from pycryptoapi.bitget import BitgetClient, BitgetAdapter


async def test_bitget_tickers(session: ClientSession):
    client = BitgetClient(session)
    raw_data = await client.ticker()
    tickers = BitgetAdapter.tickers(raw_data)
    print("Bitget tickers:", tickers)
    print("Total Bitget tickers:", len(tickers))


async def test_bitget_futures_tickers(session: ClientSession):
    client = BitgetClient(session)
    raw_data = await client.futures_ticker()
    futures_tickers = BitgetAdapter.futures_tickers(raw_data)
    print("Bitget futures tickers:", futures_tickers)
    print("Total Bitget futures tickers:", len(futures_tickers))


async def test_bitget_ticker_24h(session: ClientSession):
    client = BitgetClient(session)
    raw_data = await client.ticker()
    ticker_24h = BitgetAdapter.ticker_24h(raw_data)
    print("Bitget 24h ticker:", ticker_24h)
    print("Total Bitget 24h tickers:", len(ticker_24h))


async def test_bitget_futures_ticker_24h(session: ClientSession):
    client = BitgetClient(session)
    raw_data = await client.futures_ticker(symbol="BTC-USDT")
    futures_ticker_24h = BitgetAdapter.futures_ticker_24h(raw_data)
    print("Bitget 24h futures ticker:", futures_ticker_24h)
    print("Total Bitget 24h futures tickers:", len(futures_ticker_24h))


# To run all the tests for Bitget
async def test_bitget(session: ClientSession):
    await test_bitget_tickers(session)
    await test_bitget_futures_tickers(session)
    await test_bitget_ticker_24h(session)
    await test_bitget_futures_ticker_24h(session)


# Running the tests for Bitget
async def main():
    async with ClientSession() as session:
        await test_bitget(session)


if __name__ == "__main__":
    asyncio.run(main())
