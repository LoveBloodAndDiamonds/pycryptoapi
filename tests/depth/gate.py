import asyncio

from pycryptoapi import GateClient


async def main() -> None:
    cl = await GateClient.create()

    r = await cl.depth("BTC_USDT", 10)

    import pprint

    pprint.pp(r)

    await cl.close()


if __name__ == '__main__':
    asyncio.run(main())
