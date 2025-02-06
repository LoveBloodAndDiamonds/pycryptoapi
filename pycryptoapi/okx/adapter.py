from typing import Any, List, Dict, Union

from ..abstract import AbstractAdapter
from ..exc import AdapterException
from ..types import TickerDailyItem, KlineDict, OpenInterestItem


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
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
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

                ticker_data[symbol] = TickerDailyItem(
                    p=round(p_change, 2),  # Процентное изменение
                    v=int(float(item["volCcy24h"]))  # Объём торгов в валюте котировки
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

                ticker_data[symbol] = TickerDailyItem(
                    p=round(p_change, 2),  # Процентное изменение
                    v=int(float(item["volCcy24h"]))  # Объём торгов в валюте котировки
                )
            return ticker_data

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
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

                ticker_data[symbol] = TickerDailyItem(
                    p=round(p_change, 2),  # Процентное изменение
                    v=int(float(item["volCcy24h"]))  # Объём торгов в валюте котировки
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

                ticker_data[symbol] = TickerDailyItem(
                    p=round(p_change, 2),  # Процентное изменение
                    v=int(float(item["volCcy24h"]))  # Объём торгов в валюте котировки
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

    @staticmethod
    def kline_message(raw_msg: Any) -> List[KlineDict]:
        """
        Преобразует сырое сообщение с вебсокета OKX в унифицированный формат свечи (Kline).

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Список унифицированных объектов Kline.
        :raises AdapterException: Если сообщение имеет неверную структуру или данные невозможно преобразовать.
        """
        try:
            symbol = raw_msg["arg"]["instId"].replace("-", "")  # Убираем дефисы из символа
            timeframe = raw_msg["arg"]["channel"].replace("candle", "")  # Извлекаем таймфрейм
            klines = []

            for data in raw_msg["data"]:
                klines.append(KlineDict(
                    s=symbol,
                    t=int(data[0]),
                    o=float(data[1]),
                    h=float(data[2]),
                    l=float(data[3]),
                    c=float(data[4]),
                    v=float(data[7]),  # Используем "quote volume" (USDT)  # todo OKX futures returns SWAP-CONTRACTS
                    i=timeframe,
                    T=None,  # Добавляем 60 сек, так как таймфрейм 1 мин
                    x=None,  # OKX всегда отправляет закрытые свечи
                ))

            return klines
        except KeyError as e:
            raise AdapterException(f"Missing key in OKX kline message: {e}")
        except (TypeError, ValueError) as e:
            raise AdapterException(f"Invalid data format in OKX kline message: {e}")

    @staticmethod
    def open_interest(raw_data: Dict[str, Any]) -> Dict[str, OpenInterestItem]:
        raise NotImplementedError("Not implemented yet...")
