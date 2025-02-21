__all__ = ["AbstractAdapter", ]

from abc import ABC, abstractmethod
from typing import List, Any, Dict

from ..types import TickerDailyItem, KlineDict, OpenInterestItem, AggTradeDict, LiquidationDict


class AbstractAdapter(ABC):
    """
    Абстрактный класс адаптера для преобразования сырых данных с бирж в унифицированный вид.

    Этот класс задаёт интерфейс для реализации адаптеров, которые преобразуют данные
    из различных API бирж в стандартизированный формат.
    """

    @staticmethod
    @abstractmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные тикеров в список символов.

        :param raw_data: Сырые данные тикеров.
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "USDT".
        :return: Список символов тикеров.
        """
        pass

    @staticmethod
    @abstractmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные фьючерсных тикеров в список символов.

        :param raw_data: Сырые данные фьючерсных тикеров.
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "USDT".
        :return: Список символов фьючерсных тикеров.
        """
        pass

    @staticmethod
    @abstractmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров в унифицированный вид.

        :param raw_data: Сырые данные статистики.
        :param only_usdt: Если True, возвращает только статистику тикеров, оканчивающихся на "USDT".
        :return: Словарь с тикерами и их 24-часовой статистикой.
        """
        pass

    @staticmethod
    @abstractmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсов.
        :param only_usdt: Если True, возвращает только статистику тикеров, оканчивающихся на "USDT".
        :return: Словарь с фьючерсными тикерами и их 24-часовой статистикой.
        """
        pass

    @staticmethod
    @abstractmethod
    def funding_rate(raw_data: Any, **kwargs) -> Dict[str, float]:
        """
        Преобразует сырые данные ставки финансирования для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные ставки финансирования фьючерсов.
        :return: Словарь с фьючерсными тикерами и значением их ставки финансирования.
        """
        pass

    @staticmethod
    @abstractmethod
    def open_interest(raw_data: Dict[str, Any]) -> Dict[str, OpenInterestItem]:
        """
        Преобразует сырые данные открытого интереса в унифицированный вид.

        :param raw_data: Сырые данные открытого интереса по тикеру.
        :return: Cловарь с фьючерсными тикерами и их ставкой финансирования.
        """
        pass

    @staticmethod
    @abstractmethod
    def kline_message(raw_msg: Any) -> List[KlineDict]:
        """
        Преобразует сырое сообщение с вебсокета в унифицированный вид.
        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный обьект List[KlineDict], или None, если сообщение невалидно.
        :raises: AdapterException если возникла ошибка при унификации данных.
        """
        pass

    @staticmethod
    @abstractmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        """
        Преобразует сырое сообщение с вебсокета в унифицированный вид.
        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный обьект List[AggTradesDict], или None, если сообщение невалидно.
        :raises: AdapterException если возникла ошибка при унификации данных.
        """
        pass

    @staticmethod
    @abstractmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        """
        Преобразует сырое сообщение с вебсокета в унифицированный вид.
        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект List[LiquidationDict], или None, если сообщение невалидно.
        """
        pass
