__all__ = ["AbstractClient", "BaseClient", ]

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Union, Literal, Self

import aiohttp
import loguru
from loguru._logger import Logger  # noqa

from ..types import JsonLike


class ClientMixin:

    @staticmethod
    def filter_params(params: Dict) -> Dict:
        return {k: v for k, v in params.items() if v is not None}


class BaseClient(ABC, ClientMixin):
    """
    Базовый класс для создания клиентов для работы с API.

    Параметры:
        session (aiohttp.ClientSession): Сессия для выполнения HTTP-запросов.
        logger (Logger): Логгер для вывода информации.
        request_kwargs (dict): Дополнительные аргументы для передачи в запросы (например, заголовки).
    """

    def __init__(
            self,
            session: aiohttp.ClientSession,
            logger: logging.Logger | Logger = loguru.logger,
            max_retries: Optional[int] = 3,
            retry_delay: Optional[int | float] = 0.1,
    ) -> None:
        self._session: aiohttp.ClientSession = session
        self._logger: logging.Logger | Logger = logger
        self._max_retries: int = max(max_retries, 1)
        self._retry_delay: int | float = max(retry_delay, 0)

    @classmethod
    async def create(
            cls,
            session: Optional[aiohttp.ClientSession] = None,
            logger: logging.Logger | Logger = loguru.logger,
            max_retries: Optional[int] = 3,
            retry_delay: Optional[int | float] = 0.1,
    ) -> Self:
        """
        Создает инстанцию клиента.
        Создать клиент можно и через __init__, но в таком случае session: aiohttp.ClientSession - обязательный параметр.
        :return:
        """
        return cls(
            session=session or aiohttp.ClientSession(),
            logger=logger,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

    async def _make_request(
            self,
            method: Literal["GET", "POST", "PUT", "DELETE"],
            url: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], List[Any]]:
        """
        Выполняет HTTP-запрос к API биржи.

        Параметры:
            method (RequestMethod): HTTP-метод запроса (GET, POST).
            endpoint (str): Конечная точка API (например, "/ticker").
            params (dict, optional): Параметры запроса.
            data (dict, optional): Данные для POST-запроса.
            headers (dict, optional): Заголовки запроса.

        Возвращает:
            dict или list: Ответ API в формате JSON.
        """
        self._logger.debug(f"Request: {method} {url} | Params: {params} | Headers: {headers}")

        for attempt in range(1, self._max_retries + 1):
            try:
                async with self._session.request(
                        method=method,
                        url=url,
                        params=params,
                        headers=headers
                ) as response:
                    return await self._handle_response(response=response)

            except (aiohttp.ServerTimeoutError, aiohttp.ConnectionTimeoutError) as e:
                self._logger.debug(f"Attempt {attempt}/{self._max_retries} failed: {type(e)} -> {e}")
                if attempt < self._max_retries:
                    await asyncio.sleep(self._retry_delay)
                else:
                    self._logger.error("Max retries reached. Giving up.")
                    raise TimeoutError(f"Timeout error after {self._max_retries} request on {method} {url}")

    async def _handle_response(self, response: aiohttp.ClientResponse) -> JsonLike:
        """
        Функция обрабатывает ответ от HTTP запроса.
        :return:
        """
        response.raise_for_status()
        result = await response.json()

        # try to log result if it's not too large
        try:
            result_str: str = str(result)
            self._logger.debug(f"Response: {result_str[:100]} {'...' if len(result_str) > 100 else ''}")
        except Exception as e:
            self._logger.error(f"Error while log response: {e}")

        return result

    def __str__(self) -> str:
        return f"APIClient"

    def __repr__(self) -> str:
        return f"<APIClient>"


class AbstractClient(BaseClient, ABC):
    """Абстрактный класс для создания клиентов для работы с API криптобирж."""

    @abstractmethod
    async def ticker(self, *args, **kwargs) -> Any:
        """Возвращает JSON, в котором содержится информация о изменении цены и объеме монет за 24ч."""
        pass

    @abstractmethod
    async def futures_ticker(self, *args, **kwargs) -> Any:
        """Возвращает JSON, в котором содержится информация о изменении цены и объеме монет за 24ч."""
        pass

    @abstractmethod
    async def funding_rate(self, *args, **kwargs) -> Any:
        """Возвращает JSON, в котором содержится информация о ставке финансирования."""
        pass

    @abstractmethod
    async def open_interest(self, *args, **kwargs) -> Any:
        """Возаращает JSON, в котором содержится информация об открытом интересе."""
        pass
