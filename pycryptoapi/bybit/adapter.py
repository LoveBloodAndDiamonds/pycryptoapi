from typing import Any, List, Dict

from ..abstract import AbstractAdapter
from ..types import Ticker24hItem


class BybitAdapter(AbstractAdapter):
    """
    Адаптер для преобразования сырых данных Bybit в унифицированный вид.
    """

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные тикеров Bybit в список символов.

        :param raw_data: Сырые данные тикеров (словарь с ключом "result").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "USDT".
        :return: Список символов тикеров.
        """
        if only_usdt:
            tickers = []
            for item in raw_data.get("result", {}).get("list"):
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers.append(symbol)
            return tickers
        else:
            return [item["symbol"] for item in raw_data["result"]]

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные фьючерсных тикеров Bybit в список символов.

        :param raw_data: Сырые данные фьючерсных тикеров (словарь с ключом "result").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "USDT".
        :return: Список символов фьючерсных тикеров.
        """
        return BybitAdapter.tickers(raw_data, only_usdt)

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров Bybit в унифицированный вид.

        :param raw_data: Сырые данные статистики (словарь с ключом "result").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "USDT".
        :return: Словарь с тикерами и их 24-часовой статистикой.
        """
        if only_usdt:
            ticker_data = {}
            for item in raw_data.get("result", {}).get("list"):
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    ticker_data[symbol] = Ticker24hItem(
                        p=float(item["price24hPcnt"]) * 100,  # Изменение цены в процентах за 24ч
                        v=float(item["volume24h"])  # Объем за 24ч
                    )
            return ticker_data
        else:
            return {
                item["symbol"]: Ticker24hItem(
                    p=float(item["price24hPcnt"]) * 100,  # Изменение цены в процентах за 24ч
                    v=float(item["volume24h"])  # Объем за 24ч
                ) for item in raw_data["result"]
            }

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров Bybit в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсных тикеров (словарь с ключом "result").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "USDT".
        :return: Словарь с фьючерсными тикерами и их 24-часовой статистикой.
        """
        return BybitAdapter.ticker_24h(raw_data, only_usdt)
