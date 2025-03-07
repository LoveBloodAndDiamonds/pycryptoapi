import asyncio

import aiohttp

from pycryptoapi.bybit import BybitClient, BybitAdapter


async def test_bybit_tickers():
    async with aiohttp.ClientSession() as session:
        client = BybitClient(session)
        raw_data = await client.ticker()

        # Преобразуем данные через адаптер
        tickers = BybitAdapter.tickers(raw_data)
        print("Processed tickers:", tickers)
        print("Number of spot tickers:", len(tickers))


async def test_bybit_futures_tickers():
    async with aiohttp.ClientSession() as session:
        client = BybitClient(session)
        raw_data = await client.futures_ticker()

        from pprint import pp
        pp(raw_data)

        # Преобразуем данные через адаптер
        futures_tickers = BybitAdapter.futures_tickers(raw_data)
        print("Processed futures tickers:", futures_tickers)
        print("Number of futures tickers:", len(futures_tickers))


async def test_bybit_ticker_24h():
    async with aiohttp.ClientSession() as session:
        client = BybitClient(session)
        raw_data = await client.ticker()

        # Преобразуем данные через адаптер
        ticker_24h_data = BybitAdapter.ticker_24h(raw_data)
        print("Processed 24h ticker data:", ticker_24h_data)
        print("Number of 24h spot tickers:", len(ticker_24h_data))


async def test_bybit_futures_ticker_24h():
    async with aiohttp.ClientSession() as session:
        client = BybitClient(session)
        raw_data = await client.futures_ticker()

        # Преобразуем данные через адаптер
        futures_ticker_24h_data = BybitAdapter.futures_ticker_24h(raw_data)
        print("Processed 24h futures ticker data:", futures_ticker_24h_data)
        print("Number of 24h futures tickers:", len(futures_ticker_24h_data))


# Запуск тестов
# asyncio.run(test_bybit_tickers())
# asyncio.run(test_bybit_futures_tickers())
# asyncio.run(test_bybit_ticker_24h())
asyncio.run(test_bybit_futures_ticker_24h())
