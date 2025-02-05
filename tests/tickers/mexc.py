import asyncio

import aiohttp

from pycryptoapi.mexc import MexcClient, MexcAdapter


async def test_mexc_tickers():
    async with aiohttp.ClientSession() as session:
        client = MexcClient(session)
        raw_data = await client.ticker()

        # Преобразуем данные через адаптер
        tickers = MexcAdapter.tickers(raw_data)
        print("Processed tickers:", tickers)
        print("Number of spot tickers:", len(tickers))


async def test_mexc_futures_tickers():
    async with aiohttp.ClientSession() as session:
        client = MexcClient(session)
        raw_data = await client.futures_ticker()

        futures_tickers = MexcAdapter.futures_tickers(raw_data)
        print("Processed futures tickers:", futures_tickers)
        print("Number of futures tickers:", len(futures_tickers))


async def test_mexc_ticker_24h():
    async with aiohttp.ClientSession() as session:
        client = MexcClient(session)
        raw_data = await client.ticker()

        # Преобразуем данные через адаптер
        ticker_24h_data = MexcAdapter.ticker_24h(raw_data)
        print("Processed 24h ticker data:", ticker_24h_data)
        print("Number of 24h spot tickers:", len(ticker_24h_data))


async def test_mexc_futures_ticker_24h():
    async with aiohttp.ClientSession() as session:
        client = MexcClient(session)
        raw_data = await client.futures_ticker()

        # Преобразуем данные через адаптер
        futures_ticker_24h_data = MexcAdapter.futures_ticker_24h(raw_data)
        print("Processed 24h futures ticker data:", futures_ticker_24h_data)
        print("Number of 24h futures tickers:", len(futures_ticker_24h_data))


# Запуск тестов
# asyncio.run(test_mexc_tickers())
asyncio.run(test_mexc_futures_tickers())
# asyncio.run(test_mexc_ticker_24h())
# asyncio.run(test_mexc_futures_ticker_24h())
