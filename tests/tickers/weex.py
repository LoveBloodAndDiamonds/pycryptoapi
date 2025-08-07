import asyncio

from pycryptoapi.weex.client import WeexClient


async def main() -> None:
    client = await WeexClient.create()

    try:
        tickers = await client.ticker()

        from pprint import pp

        pp(tickers)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())

# curl "https://api-contract.weex.com/capi/v2/market/tickers"
# curl "https://api-contract.weex.com/capi/v2/market/tickers"
# curl "https://api-contract.weex.com/capi/v2/market/time"