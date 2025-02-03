__all__ = ["AbstractWebsocket", "AbstractSocketManager", ]

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import List, Callable, Optional, Awaitable, Union

import loguru
import orjson
import websockets
from loguru._logger import Logger  # noqa
from websockets.asyncio.client import ClientConnection

from ..enums import MarketType


class AbstractWebsocket(ABC):
    """
    Базовый класс для подключения к WebSocket и обработки потоков данных.

    На данный момент задача стоит в том, чтобы поддерживать 4 типа соединений для обоих типов рынков:
    - Свечи
    - Аггрегированные сделки
    - Ликвидации (устарело, ликвидации с криптобирж приходят некорректные, идея отложена)
    - Тикеры (объем, изменение цены за 24ч и пр. общая информация)

    Параметры:
        market_type (MarketType): Тип рынка.
        tickers (List[str]): Список тикеров для подписки.
        callback (Callable[..., Awaitable]): Асинхронная функция обратного вызова для обработки сообщений.
        logger (logging.Logger | loguru._logger.Logger): Логгер для вывода информации.
        ping_interval (int): Интервал отправки ping-сообщений.
        reconnect_interval (int): Интервал для повторного подключения при ошибке.
        **kwargs (dict): Аргументы для вебсокет-соединения.
    """

    def __init__(
            self,
            topic: str,
            callback: Callable[..., Awaitable],
            market_type: Optional[MarketType] = None,
            tickers: Optional[List[str]] = None,
            timeframe: Optional[str] = None,
            logger: Union[logging.Logger, Logger] = loguru.logger,
            ping_interval: int = 30,
            reconnect_interval: int = 60,
            **ws_kwargs  # websocket kwargs
    ) -> None:
        self._topic: str = topic
        self._callback: Callable = callback
        self._market_type: Optional[MarketType] = market_type
        self._tickers: Optional[List[str]] = tickers
        self._timeframe: Optional[str] = timeframe
        self._ping_interval: int = ping_interval
        self._reconnect_interval: int = reconnect_interval
        self._logger: logging.Logger | Logger = logger

        # Задача для отправки ping-сообщений
        self._curr_ping_task: Optional[asyncio.Task] = None

        # Аргументы для подключения к websocket.connect
        self._ws_kwargs: Optional[dict] = dict(
            ping_interval=self._ping_interval,
            close_timeout=0.1,
            **ws_kwargs
        )

        # Флаг активности подключения
        self._is_active: bool = False

    @property
    @abstractmethod
    def _connection_uri(self) -> str:
        """Абстрактное свойство: URI для подключения к WebSocket. Если подключение к топику(ам) происходит через
        uri - то нужно указать его тут. Иначе оно указывается в _subscribe_message."""
        ...

    @property
    @abstractmethod
    def _ping_message(self) -> Optional[str]:
        """Абстрактное свойство: Сообщение ping. (JSON). websockets предоставляет автоматический PING и PONG, это
        свойство нужно указывать, если сервис требует кастомного PING сообщения."""
        ...

    @property
    @abstractmethod
    def _subscribe_message(self) -> Optional[Union[str, List[str]]]:
        """Абстрактное свойство: Сообщение для подписки. (JSON). Если подключение к топику(ам) происходит через отправку
        JSON - то нужно указать это свойство. Иначе оно указывается в _connection_uri.
        Если тип возвращаемых данных - List - то значит биржа не поддерживает множественные аргументы и нужно отправить
        несколько сообщений с подпиской на топик.
        """
        ...

    async def _connect(self):
        """
        Подключение к WebSocket серверу и прослушивание потоков данных.
        """
        while self._is_active:
            # Логируем запуск
            self._logger.info(f"{self} Starting connection")

            # Отменяем предыдущую задачу ping (если есть)
            if self._curr_ping_task:
                self._curr_ping_task.cancel()

            try:

                uri: str = self._connection_uri
                self._logger.debug(f"{self} Estabilishing connection with {uri}")
                async with websockets.connect(uri=uri, **self._ws_kwargs) as websocket:
                    self._logger.debug(f"{self} Connected {uri}")

                    # Отправляем сообщение для подписки
                    await self._subscribe(websocket)

                    # Запускаем задачу для ping
                    if self._ping_message:
                        self._curr_ping_task = asyncio.create_task(self._ping_task(websocket))

                    # Прослушиваем сообщения
                    await self._handler(websocket)

            except Exception as e:
                self._logger.exception(
                    f"{self} Connection error: {e}. Reconnecting in {self._reconnect_interval} seconds.")
                await asyncio.sleep(self._reconnect_interval)

    async def _handler(self, conn: ClientConnection) -> None:
        """
        Принимает управление над активным подключением.

        Параметры:
            conn (ClientConnection): Активное WebSocket соединение.
        """
        # Слушаем входящие сообщения
        while self._is_active:
            try:
                message = await conn.recv()
                self._logger.trace(f"{self} Received message: {message}")
                await self._callback(orjson.loads(message))
            except orjson.JSONDecodeError:
                if message not in ["ping", "pong"]:
                    self._logger.error(f"{self} orjson.JSONDecodeError whilte handling message: {message}")
                else:
                    self._logger.debug(f"{self} Received ping message: {message}")
            except Exception as e:
                self._logger.error(f"{self} Error({type(e)}) while handling message: {e}")
                break

    async def _ping_task(self, conn: ClientConnection) -> None:
        """
        Отправляет ping-сообщения на сервер WebSocket.

        Параметры:
            conn (ClientConnection): Активное WebSocket соединение.
        """
        while self._is_active:
            try:
                if self._ping_message:
                    await conn.send(self._ping_message)
                    self._logger.debug(f"{self} Ping sent.")
            except Exception as e:
                self._logger.exception(f"{self} Error({type(e)}) while sending ping: {e}")
            finally:
                await asyncio.sleep(self._ping_interval)

    async def _subscribe(self, conn: ClientConnection) -> None:
        """
        Отправляет сообщение для подписки на сервер WebSocket.

        Параметры:
            conn (ClientConnection): Активное WebSocket соединение.
        """
        try:
            subscribe_message: Union[str, List[str]] = self._subscribe_message
            if subscribe_message:
                if isinstance(subscribe_message, str):
                    subscribe_message: List[str] = [subscribe_message]
                for message in subscribe_message:
                    await conn.send(message)
                    self._logger.debug(f"{self} Sent subscribe message: {message}")
            else:
                self._logger.debug(f"{self} No subscription message defined.")
        except Exception as e:
            self._logger.error(f"{self} Failed to send subscribe message: {e}")

    async def start(self):
        """
        Запускает процесс подключения и обработки сообщений.
        """
        if self._is_active:
            raise RuntimeError(f"Can not be runned more than once")
        else:
            self._is_active: bool = True

        while self._is_active:
            try:
                await self._connect()
            except Exception as e:
                self._logger.error(f"{self} Unexpected exception ({type(e)}): {e}."
                                   f" Reconnecting after {self._reconnect_interval} seconds.")
                await asyncio.sleep(self._reconnect_interval)

    async def stop(self) -> None:
        """
        Останавливает WebSocket.
        """
        self._is_active = False
        if self._curr_ping_task:
            self._curr_ping_task.cancel()

    def __str__(self) -> str:
        return f"[Websocket {self._market_type} {self._topic} {len(self._tickers) if self._tickers else '' or '*'}Xtickers]"

    def __repr__(self) -> str:
        return f"<Websocket {self._market_type} {self._topic}>"


class AbstractSocketManager(ABC):
    """Абстрактный менеджер для создания вебсокет соединений к определенным топикам."""

    @classmethod
    @abstractmethod
    def klines_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        """Возвращает обьект, который позволяет подключаться к Klines вебсокету."""
        pass

    @classmethod
    @abstractmethod
    def aggtrades_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        """Возвращает обьект, который позволяет подключаться к Aggtrades вебсокету."""
        pass

    @classmethod
    @abstractmethod
    def tickers_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        """Возвращает обьект, который позволяет подключаться к Tickers вебсокету."""
        pass
