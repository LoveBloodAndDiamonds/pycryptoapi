import asyncio

from pycryptoapi import MexcClient


async def main() -> None:
    cl = await MexcClient.create()

    r = await cl.depth("BTCUSDT", 3)

    import pprint

    pprint.pp(r)

    await cl.close()


if __name__ == '__main__':
    asyncio.run(main())
