# PyCryptoAPI

**PyCryptoAPI** — это асинхронный коннектор API для работы с различными централизованными криптовалютными биржами и
криптовалютными сервисами. Он предоставляет единый интерфейс для получения рыночных данных на нескольких платформах.

## Поддерживаемые биржи

- Binance
- Bybit
- Bitget
- OKX
- MEXC
- Deribit

## Поддерживаемые сервисы

- Coinalyze
- Coinmarketcap

## Установка

Для установки PyCryptoAPI можно использовать `pip` или `poetry` или `uv`.

### Использование pip

```bash
pip install git+https://github.com/LoveBloodAndDiamonds/pycryptoapi.git@main
```

### Использование poetry

```bash
poetry add git+https://github.com/LoveBloodAndDiamonds/pycryptoapi.git
```

### Использование uv

```bash
uv add git+https://github.com/LoveBloodAndDiamonds/pycryptoapi.git
```

## Использование

##### Пример получения информации о тикерах с OKX:

```python
import asyncio

from pycryptoapi import OkxClient, OkxAdapter


async def main():
    # Инициализация клиента
    client = await OkxClient.create()

    # Получение информации о фьючерсных тикерах
    tickers = await client.futures_ticker()

    # Адаптер содержит функции, которые приводят сырые данные в единый вид для всех бирж.
    # Это удобно при разработке приложения, которое должно одинаково работать сразу
    # с несколькими рынками.
    tickers_24h = OkxAdapter.futures_ticker_24h(raw_data=tickers, only_usdt=True)

    # Вывод данных
    for symbol, data in tickers_24h.items():
        print(symbol, data)

    # Закрытие сессии aiohttp
    await client.close()


# Запуск
asyncio.run(main())
```

### Разбор кода:

- Импортируются необходимые модули и классы.
- Инициализируется клиент для работы с OKX.
- Вызывается метод `futures_ticker()` для получения актуальной информации о тикерах.
- Данные адаптируются в соответствии с нужной задачей. Один и тот же тип сырых данных может подходить для нескольких
  задач в зависимости от биржи.

##### Пример подключения к вебсокету:

```python
import asyncio

from pycryptoapi import MexcSocketManager, MexcAdapter
from pycryptoapi.enums import MarketType, Timeframe
from pycryptoapi.exc import AdapterException
from pycryptoapi.types import KlineDict


async def main():
    socket = MexcSocketManager.klines_socket(
        market_type=MarketType.SPOT,
        timeframe=Timeframe.MIN_1,
        tickers=["BTCUSDT", "ETHUSDT"],
        callback=callback
    )

    await socket.start()


async def callback(msg):
    try:
        # У каждой биржи есть свой адаптер, который приводит данные в единый формат.
        # Так, например, мы можем иметь одинаковый объект KlineDict для любой биржи.
        kline: KlineDict = MexcAdapter.kline_message(raw_msg=msg)
        print(kline)

    except AdapterException as e:
        print(f"Can not adapt message ({e}): {msg}")


asyncio.run(main())
```

### Разбор кода:

- Импортируются необходимые модули и классы.
- Инициализируется клиент для работы с Mexc.
- Создается объект MexcWebsocket, с помощью MexcSocketManager
- MexcWebsocket запускается методом start()
- Данные приходят в указанную в парамтре callback асинхронную функцию.
- Данные адаптируются в унифицированный вид.

## Вклад в разработку

Если у вас есть предложения или исправления, вы можете открыть Issue или Pull Request
в [GitHub-репозитории](https://github.com/LoveBloodAndDiamonds/pycryptoapi).

## Предупреждение

‼️ Автор не несет никакой ответственности за проблемы, которые могут возникнуть в процессе использования этого кода.

‼️ Автор имеет право вносить изменения в любое время.
