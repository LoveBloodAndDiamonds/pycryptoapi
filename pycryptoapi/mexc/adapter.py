from typing import Any, List, Dict

from ..abstract import AbstractAdapter
from ..types import Ticker24hItem


class MexcAdapter(AbstractAdapter):
    """
    Адаптер для преобразования сырых данных MEXC в унифицированный вид.
    """

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные тикеров MEXC в список символов.

        :param raw_data: Сырые данные тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "USDT".
        :return: Список символов тикеров.
        """
        if only_usdt:
            tickers = []
            for item in raw_data:
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers.append(symbol)
            return tickers
        return [item["symbol"] for item in raw_data]

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные фьючерсных тикеров MEXC в список символов.

        :param raw_data: Сырые данные фьючерсных тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "_USDT".
        :return: Список символов фьючерсных тикеров.
        """
        if only_usdt:
            tickers = []
            for item in raw_data["data"]:
                symbol = item["symbol"]
                if symbol.endswith("_USDT"):
                    tickers.append(symbol)
            return tickers
        return [item["symbol"] for item in raw_data]

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров MEXC в унифицированный вид.

        :param raw_data: Сырые данные статистики (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "USDT".
        :return: Словарь с тикерами и их 24-часовой статистикой.
        """
        if only_usdt:
            ticker_data = {}
            for item in raw_data:
                symbol = item["symbol"]
                if not symbol.endswith("USDT"):
                    continue

                ticker_data[symbol] = Ticker24hItem(
                    p=float(item["priceChangePercent"]) * 100,  # Конвертируем в проценты
                    v=float(item["quoteVolume"])  # Объём торгов в валюте котировки
                )
            return ticker_data
        else:
            return {
                item["symbol"]: Ticker24hItem(
                    p=float(item["priceChangePercent"]) * 100,  # Конвертируем в проценты
                    v=float(item["quoteVolume"])  # Объём торгов в валюте котировки
                ) for item in raw_data
            }

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров MEXC в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсных тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "_USDT".
        :return: Словарь с фьючерсными тикерами и их 24-часовой статистикой.
        """
        if only_usdt:
            ticker_data = {}
            for item in raw_data["data"]:
                symbol = item["symbol"]
                if not symbol.endswith("_USDT"):
                    continue
                avg_price = (float(item["high24Price"]) + float(item["lower24Price"])) / 2
                price_change = ((float(item["lastPrice"]) - avg_price) / avg_price) * 100 if avg_price != 0 else 0
                ticker_data[symbol] = Ticker24hItem(
                    p=price_change,  # Процентное изменение
                    v=float(item["volume24"])
                )
            return ticker_data
        else:
            ticker_data = {}
            for item in raw_data["data"]:
                symbol = item["symbol"]
                avg_price = (float(item["high24Price"]) + float(item["lower24Price"])) / 2
                price_change = ((float(item["lastPrice"]) - avg_price) / avg_price) * 100 if avg_price != 0 else 0
                ticker_data[symbol] = Ticker24hItem(
                    p=price_change,  # Процентное изменение
                    v=float(item["volume24"])
                )
            return ticker_data
