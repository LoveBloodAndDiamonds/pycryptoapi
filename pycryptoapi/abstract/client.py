__all__ = ["AbstractClient", "BaseClient", ]

import logging
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Union, Literal

import aiohttp
import loguru
from loguru._logger import Logger  # noqa


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
    ) -> None:
        self._session: aiohttp.ClientSession = session
        self._logger: logging.Logger | Logger = logger

    async def _make_request(
            self,
            method: Literal["GET", "POST", "PUT", "DELETE"],
            url: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None
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

        try:
            async with self._session.request(
                    method=method,
                    url=url,
                    params=params,
                    headers=headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                self._logger.debug(f"Response: {result}")
                return result
        except aiohttp.ClientError as e:
            self._logger.error(f"Request error ({type(e)}): {e}")
            raise
        except Exception as e:
            self._logger.error(f"Unexpected error: {e}")
            raise

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
    async def funding_rate(self, *args, **kwargs) -> None:
        """Возвращает JSON, в котором содержится информация о ставке финансирования."""
        pass
