import asyncio

from pycryptoapi import GateClient

from pprint import pp

proxies = ["http://JxTqUZB07C:Rz0XwsaGDa@194.31.73.78:53015"]


async def main() -> None:

    try:
        client = await GateClient.create(proxies=proxies)

        response = await client.open_interest(symbol="BTC_USDT")

        pp(response)
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())


# import aiohttp
# import asyncio
#
# proxy = "http://JxTqUZB07C:Rz0XwsaGDa@194.31.73.78:53015"
#
#
# async def test_proxy(proxy: str):
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get("http://httpbin.org/ip", proxy=proxy, timeout=aiohttp.ClientTimeout(total=5)) as resp:
#                 print(await resp.text())
#     except Exception as e:
#         print(f"❌ Proxy failed: {proxy} — {e}")
#
# asyncio.run(test_proxy(proxy))