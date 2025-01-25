__all__ = ["AbstractAdapter", ]

from abc import ABC, abstractmethod
from typing import List, Any, Dict

from ..types import Ticker24hItem


class AbstractAdapter(ABC):
    """Адаптер для преобразования сырых данных с бирж и ресурсов в унифицированный вид."""

    @staticmethod
    @abstractmethod
    def process_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """Преобразовывает сырой ответ по тикерам в список тикеров."""
        pass

    @staticmethod
    @abstractmethod
    def process_futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """Преобразовывает сырой ответ по фьючерсным тикерам в список тикеров."""
        pass

    @staticmethod
    @abstractmethod
    def process_ticker24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        pass

    @staticmethod
    @abstractmethod
    def process_futures_ticker24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        pass
