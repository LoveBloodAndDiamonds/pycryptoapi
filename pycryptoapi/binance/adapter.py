from typing import Any, List, Dict

from ..abstract import AbstractAdapter
from ..types import Ticker24hItem


class BinanceAdapter(AbstractAdapter):
    @staticmethod
    def process_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Обрабатывает сырые данные тикеров, фильтруя только те, которые заканчиваются на "USDT".

        :param raw_data: Сырые данные о тикерах (список словарей).
        :param only_usdt: Если True, возвращаются только тикеры, заканчивающиеся на "USDT".
        :return: Список тикеров, соответствующих фильтру.
        """
        if only_usdt:
            tickers: List[str] = []
            for item in raw_data:
                symbol: str = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers.append(symbol)
            return tickers
        else:
            return [item["symbol"] for item in raw_data]

    @staticmethod
    def process_futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Обрабатывает сырые данные фьючерсных тикеров, фильтруя только те, которые заканчиваются на "USDT".

        :param raw_data: Сырые данные о фьючерсных тикерах (список словарей).
        :param only_usdt: Если True, возвращаются только тикеры, заканчивающиеся на "USDT".
        :return: Список фьючерсных тикеров, соответствующих фильтру.
        """
        return BinanceAdapter.process_tickers(raw_data, only_usdt)

    @staticmethod
    def process_ticker24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Обрабатывает сырые данные о 24-часовой статистике для спотовых тикеров.

        :param raw_data: Сырые данные 24-часовой статистики (список словарей).
        :param only_usdt: Если True, возвращаются только данные для тикеров, заканчивающихся на "USDT".
        :return: Словарь с тикером и его данными за 24 часа.
        """
        ticker_data: dict = {}

        for item in raw_data:
            symbol = item["symbol"]
            if only_usdt and not symbol.endswith("USDT"):
                continue

            ticker_data[symbol] = Ticker24hItem(
                p=float(item["priceChangePercent"]),  # Последняя цена
                v=float(item["quoteVolume"])  # Объем
            )

        return ticker_data

    @staticmethod
    def process_futures_ticker24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Обрабатывает сырые данные о 24-часовой статистике для фьючерсных тикеров.

        :param raw_data: Сырые данные 24-часовой статистики для фьючерсных тикеров (список словарей).
        :param only_usdt: Если True, возвращаются только данные для фьючерсных тикеров, заканчивающихся на "USDT".
        :return: Словарь с фьючерсными тикерами и их данными за 24 часа.
        """
        return BinanceAdapter.process_ticker24h(raw_data, only_usdt)
