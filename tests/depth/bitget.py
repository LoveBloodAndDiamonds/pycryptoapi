import asyncio

from pycryptoapi import BitgetClient


async def main() -> None:
    cl = await BitgetClient.create()

    r = await cl.depth("BTCUSDT", 10)

    import pprint

    pprint.pp(r)

    await cl.close()


if __name__ == '__main__':
    asyncio.run(main())
