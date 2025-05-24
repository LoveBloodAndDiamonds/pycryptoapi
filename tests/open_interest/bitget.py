import asyncio
from pprint import pprint

import aiohttp

from pycryptoapi.bitget import BitgetClient, BitgetAdapter


async def test_bitget_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = BitgetClient(session)

        res = await client.open_interest()

        # pprint(res)

        # print(len(res["data"]))

        a = BitgetAdapter.open_interest(raw_data=res)

        pprint(a)


        # res = res["data"]
        #
        # from pprint import pp
        #
        # for item in res:
        #     if item["symbol"] == "TRXUSDT":
        #         pp(item)


        # pp(r)

# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_bitget_funding_rate())
