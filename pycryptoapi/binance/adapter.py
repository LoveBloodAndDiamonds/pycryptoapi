from typing import Any, List, Dict

from ..abstract import AbstractAdapter
from ..types import Ticker24hItem


class BinanceAdapter(AbstractAdapter):

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные тикеров в список символов.

        :param raw_data: Сырые данные тикеров (список словарей).
        :param only_usdt: Если True, возвращаются только тикеры, оканчивающиеся на 'USDT'.
        :return: Список тикеров.
        """
        if only_usdt:
            tickers = []
            for item in raw_data:
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers.append(symbol)
            return tickers
        else:
            return [item["symbol"] for item in raw_data]

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные фьючерсных тикеров в список символов.

        :param raw_data: Сырые данные фьючерсных тикеров (список словарей).
        :param only_usdt: Если True, возвращаются только тикеры, оканчивающиеся на 'USDT'.
        :return: Список фьючерсных тикеров.
        """
        return BinanceAdapter.tickers(raw_data, only_usdt)

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров в унифицированный вид.

        :param raw_data: Сырые данные статистики (список словарей).
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Словарь с тикерами и их статистикой за 24 часа.
        """
        if raw_data:
            tickers_data = {}
            for item in raw_data:
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers_data[symbol] = Ticker24hItem(
                        p=float(item["priceChangePercent"]),
                        v=float(item["quoteVolume"]),
                    )
            return tickers_data
        else:
            return {
                item["symbol"]: Ticker24hItem(
                    p=float(item["priceChangePercent"]),
                    v=float(item["quoteVolume"]),
                ) for item in raw_data
            }

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсов (список словарей).
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Словарь с фьючерсными тикерами и их статистикой за 24 часа.
        """
        return BinanceAdapter.ticker_24h(raw_data, only_usdt)
