

import asyncio

import aiohttp


async def main() -> None:
    base = "https://fapi.xt.com"
    endpoint = "/future/market/v3/public/symbol/list"
    url = base + endpoint

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            r = await resp.json()

            from pprint import pp

            for item in r["result"]["symbols"]:
                # print(item)
                print(item["symbol"], float(item["contractSize"]))  # пара -> констракт сайз
                # if item["symbol"] == "btc_usdt":
                #     pp(item)

            # pp(r["result"])


if __name__ == '__main__':
    asyncio.run(main())
