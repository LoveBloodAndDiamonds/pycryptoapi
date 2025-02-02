import aiohttp
import asyncio
from pycryptoapi.binance import BinanceClient, BinanceAdapter


async def test_binance_tickers():
    async with aiohttp.ClientSession() as session:
        client = BinanceClient(session)
        raw_data = await client.ticker()
        print("Raw data for Binance spot tickers:", raw_data)

        # Преобразуем данные через адаптер
        tickers = BinanceAdapter.tickers(raw_data)
        # print("Processed tickers:", tickers)
        # print("Processed tickers:", len(tickers))


async def test_binance_futures_tickers():
    async with aiohttp.ClientSession() as session:
        client = BinanceClient(session)
        raw_data = await client.futures_ticker()
        print("Raw data for Binance futures tickers:", raw_data)

        # Преобразуем данные через адаптер
        futures_tickers = BinanceAdapter.futures_tickers(raw_data)
        print("Processed futures tickers:", futures_tickers)
        print("Processed tickers:", len(futures_tickers))


async def test_binance_ticker_24h():
    async with aiohttp.ClientSession() as session:
        client = BinanceClient(session)
        raw_data = await client.ticker()
        print("Raw data for Binance spot ticker 24h:", raw_data)

        # Преобразуем данные через адаптер
        ticker_24h_data = BinanceAdapter.ticker_24h(raw_data)
        print("Processed 24h ticker data:", ticker_24h_data)


async def test_binance_futures_ticker_24h():
    async with aiohttp.ClientSession() as session:
        client = BinanceClient(session)
        raw_data = await client.futures_ticker()
        print("Raw data for Binance futures ticker 24h:", raw_data)

        # Преобразуем данные через адаптер
        futures_ticker_24h_data = BinanceAdapter.futures_ticker_24h(raw_data)
        print("Processed 24h futures ticker data:", futures_ticker_24h_data)


# Запуск тестов
asyncio.run(test_binance_tickers())
# asyncio.run(test_binance_futures_tickers())
# asyncio.run(test_binance_ticker_24h())
# asyncio.run(test_binance_futures_ticker_24h())
