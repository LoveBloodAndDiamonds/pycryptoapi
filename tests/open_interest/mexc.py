import aiohttp

from pycryptoapi.enums import Exchange, MarketType
from pycryptoapi.mexc import MexcClient, MexcAdapter
from pprint import pprint
import asyncio

from pycryptoapi.fixes import init_fixes, mexc_perpetual_open_interest_fix


async def test_mexc_funding_rate():
    await init_fixes(Exchange.MEXC, MarketType.FUTURES)

    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = MexcClient(session)

        # Пример вызова функции funding_rate
        result = await client.open_interest()

        # Печать результата с использованием prettyprint
        result = mexc_perpetual_open_interest_fix(result)

        # for i in result["data"]:
        #     print(i["symbol"], i["holdVol"])

        a = MexcAdapter.open_interest(raw_data=result)

        pprint(a)

        print(len(a))

# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_mexc_funding_rate())
