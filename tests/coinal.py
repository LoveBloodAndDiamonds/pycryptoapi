import asyncio

from pycryptoapi.coinalyze import CoinalyzeClient


async def main():
    client = await CoinalyzeClient.create(api_keys="d022d6b2-11a4-4621-acc9-5b452cda2178")

    try:
        r = await client.liquidations(
            tickers=["BTCUSDT_PERP.A"],
            timeframe="1hour",
            limit=100,
            convert_to_usd=True
        )

        from pprint import pp

        pp(r)

    finally:
        await client.close()


asyncio.run(main())

'''

[{'name': 'Poloniex', 'code': 'P'},
 {'name': 'Vertex', 'code': 'V'},
 {'name': 'Bitforex', 'code': 'D'},
 {'name': 'Kraken', 'code': 'K'},
 {'name': 'Bithumb', 'code': 'U'},
 {'name': 'Bitstamp', 'code': 'B'},
 {'name': 'Hyperliquid', 'code': 'H'},
 {'name': 'BitFlyer', 'code': 'L'},
 {'name': 'BtcMarkets', 'code': 'M'},
 {'name': 'Bit2c', 'code': 'I'},
 {'name': 'MercadoBitcoin', 'code': 'E'},
 {'name': 'Independent Reserve', 'code': 'N'},
 {'name': 'Gemini', 'code': 'G'},
 {'name': 'Gate.io', 'code': 'Y'},
 {'name': 'Deribit', 'code': '2'},
 {'name': 'OKX', 'code': '3'},
 {'name': 'Coinbase', 'code': 'C'},
 {'name': 'Bitfinex', 'code': 'F'},
 {'name': 'Luno', 'code': 'J'},
 {'name': 'BitMEX', 'code': '0'},
 {'name': 'Phemex', 'code': '7'},
 {'name': 'WOO X', 'code': 'W'},
 {'name': 'Huobi', 'code': '4'},
 {'name': 'dYdX', 'code': '8'},
 {'name': 'Bybit', 'code': '6'},
 {'name': 'Binance', 'code': 'A'}]
 '''
