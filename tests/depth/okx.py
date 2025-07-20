import asyncio

from pycryptoapi import MexcClient, OkxClient


async def main() -> None:
    cl = await OkxClient.create()

    r = await cl.depth("BTC-USDT", 10)

    import pprint

    pprint.pp(r)

    await cl.close()


if __name__ == '__main__':
    asyncio.run(main())
