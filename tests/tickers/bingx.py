import asyncio

import aiohttp

from pycryptoapi.bingx import BingxAdapter, BingxClient


async def test_binance_tickers():
    async with aiohttp.ClientSession() as session:
        client = BingxClient(session)
        raw_data = await client.ticker()
        print("Raw data for Binance spot tickers:", raw_data)

        # Преобразуем данные через адаптер
        tickers = BingxAdapter.tickers(raw_data)
        # print("Processed tickers:", tickers)
        # print("Processed tickers:", len(tickers))


async def test_binance_futures_tickers():
    async with aiohttp.ClientSession() as session:
        client = BingxClient(session)
        raw_data = await client.futures_ticker()
        # print("Raw data for Binance futures tickers:", raw_data)

        from pprint import pp

        pp(raw_data)

        # Преобразуем данные через адаптер
        futures_tickers = BingxAdapter.futures_last_price(raw_data)
        print("Processed futures tickers:", futures_tickers)
        print("Processed tickers:", len(futures_tickers))


async def test_binance_ticker_24h():
    async with aiohttp.ClientSession() as session:
        client = BingxClient(session)
        raw_data = await client.ticker()
        print("Raw data for Binance spot ticker 24h:", raw_data)

        # Преобразуем данные через адаптер
        ticker_24h_data = BingxAdapter.ticker_24h(raw_data)
        print("Processed 24h ticker data:", ticker_24h_data)

        print(len(ticker_24h_data))


async def test_binance_futures_ticker_24h():
    async with aiohttp.ClientSession() as session:
        client = BingxClient(session)
        raw_data = await client.futures_ticker()
        print("Raw data for Binance futures ticker 24h:", raw_data)

        # Преобразуем данные через адаптер
        futures_ticker_24h_data = BingxAdapter.futures_ticker_24h(raw_data)
        print("Processed 24h futures ticker data:", futures_ticker_24h_data)

        print(len(futures_ticker_24h_data))


# Запуск тестов
# asyncio.run(test_binance_tickers())
# asyncio.run(test_binance_futures_tickers())
# asyncio.run(test_binance_ticker_24h())
asyncio.run(test_binance_futures_ticker_24h())
