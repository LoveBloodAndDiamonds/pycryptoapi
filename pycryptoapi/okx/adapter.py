from typing import Any, List, Dict, Union

from ..abstract import AbstractAdapter
from ..types import Ticker24hItem


class OkxAdapter(AbstractAdapter):
    """
    Адаптер для преобразования сырых данных OKX в унифицированный вид.
    """

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные тикеров OKX в список символов.

        :param raw_data: Сырые данные тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "-USDT".
        :return: Список символов тикеров.
        """
        if only_usdt:
            return [item["instId"] for item in raw_data["data"] if item["instId"].endswith("-USDT")]
        return [item["instId"] for item in raw_data["data"]]

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные фьючерсных тикеров OKX в список символов.

        :param raw_data: Сырые данные фьючерсных тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "-USDT-SWAP".
        :return: Список символов фьючерсных тикеров.
        """
        if only_usdt:
            return [item["instId"] for item in raw_data["data"] if item["instId"].endswith("-USDT-SWAP")]
        return [item["instId"] for item in raw_data["data"]]

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров OKX в унифицированный вид.

        :param raw_data: Сырые данные статистики (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "-USDT".
        :return: Словарь с тикерами и их 24-часовой статистикой.
        """
        if only_usdt:
            ticker_data = {}
            for item in raw_data["data"]:
                symbol = item["instId"]
                if not symbol.endswith("-USDT"):
                    continue

                # Рассчитываем изменение цены в процентах от открытия 24h
                open_price = float(item["open24h"])
                last_price = float(item["last"])
                p_change = ((last_price - open_price) / open_price) * 100

                ticker_data[symbol] = Ticker24hItem(
                    p=p_change,  # Процентное изменение
                    v=float(item["volCcy24h"])  # Объём торгов в валюте котировки
                )
            return ticker_data
        else:
            ticker_data = {}
            for item in raw_data["data"]:
                symbol = item["instId"]

                # Рассчитываем изменение цены в процентах от открытия 24h
                open_price = float(item["open24h"])
                last_price = float(item["last"])
                p_change = ((last_price - open_price) / open_price) * 100

                ticker_data[symbol] = Ticker24hItem(
                    p=p_change,  # Процентное изменение
                    v=float(item["volCcy24h"])  # Объём торгов в валюте котировки
                )
            return ticker_data

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, Ticker24hItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров OKX в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсных тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "-USDT-SWAP".
        :return: Словарь с фьючерсными тикерами и их 24-часовой статистикой.
        """
        if only_usdt:
            ticker_data = {}
            for item in raw_data["data"]:
                symbol = item["instId"]
                if not symbol.endswith("-USDT-SWAP"):
                    continue

                # Рассчитываем изменение цены в процентах от открытия 24h
                open_price = float(item["open24h"])
                last_price = float(item["last"])
                p_change = ((last_price - open_price) / open_price) * 100

                ticker_data[symbol] = Ticker24hItem(
                    p=p_change,  # Процентное изменение
                    v=float(item["volCcy24h"])  # Объём торгов в валюте котировки
                )
            return ticker_data
        else:
            ticker_data = {}
            for item in raw_data["data"]:
                symbol = item["instId"]
                # Рассчитываем изменение цены в процентах от открытия 24h
                open_price = float(item["open24h"])
                last_price = float(item["last"])
                p_change = ((last_price - open_price) / open_price) * 100

                ticker_data[symbol] = Ticker24hItem(
                    p=p_change,  # Процентное изменение
                    v=float(item["volCcy24h"])  # Объём торгов в валюте котировки
                )
            return ticker_data

    @staticmethod
    def funding_rate(raw_data: Union[List[Dict], Dict], **kwargs) -> Dict[str, float]:
        """
        Преобразует сырые данные ставки финансирования для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные ставки финансирования фьючерсов.
        :return: Словарь с фьючерсными тикерами и значением их ставки финансирования.
        """
        if isinstance(raw_data, list):
            tickers_info = {}
            for item in raw_data:
                data = item["data"][0]
                tickers_info[data["instId"]] = float(data["fundingRate"]) * 100
            return tickers_info
        elif isinstance(raw_data, dict):
            data = raw_data["data"][0]
            return {data["instId"]: float(data["fundingRate"]) * 100}
        else:
            raise TypeError(f"Wrong raw_data type: {type(raw_data)}, excepted List[Dict] or Dict")
