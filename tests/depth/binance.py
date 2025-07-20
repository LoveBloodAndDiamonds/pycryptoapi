import asyncio

from pycryptoapi import CLIENTS_MAPPER, ADAPTERS_MAPPER
from pycryptoapi.enums import Exchange

e = Exchange.BITGET

# bitget ?


async def main() -> None:
    client = await CLIENTS_MAPPER[e].create()
    adapter = ADAPTERS_MAPPER[e]

    raw_data = await client.depth("BTCUSDT", 10)

    print(raw_data)

    data = adapter.depth(raw_data=raw_data)

    import pprint

    pprint.pp(data)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
