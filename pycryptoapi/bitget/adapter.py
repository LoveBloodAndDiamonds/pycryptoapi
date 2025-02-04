from typing import Any, List, Dict, Union

from ..abstract import AbstractAdapter
from ..exc import AdapterException
from ..types import TickerDailyItem, KlineDict


class BitgetAdapter(AbstractAdapter):
    """
    Адаптер для преобразования сырых данных Bitget в унифицированный вид.
    """

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные тикеров Bitget в список символов.

        :param raw_data: Сырые данные тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "USDT".
        :return: Список символов тикеров.
        """
        if only_usdt:
            tickers = []
            for item in raw_data.get("data", []):
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers.append(symbol)
            return tickers
        return [item["symbol"] for item in raw_data.get("data", [])]

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные фьючерсных тикеров Bitget в список символов.

        :param raw_data: Сырые данные фьючерсных тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "USDT".
        :return: Список символов фьючерсных тикеров.
        """
        return BitgetAdapter.tickers(raw_data=raw_data, only_usdt=only_usdt)

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров Bitget в унифицированный вид.

        :param raw_data: Сырые данные статистики (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "USDT".
        :return: Словарь с тикерами и их 24-часовой статистикой.
        """
        if only_usdt:
            ticker_data = {}
            for item in raw_data.get("data", []):
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    ticker_data[symbol] = TickerDailyItem(
                        p=round(float(item["change24h"]) * 100, 2),  # Конвертируем в проценты
                        v=int(float(item["usdtVolume"]))  # Объем торгов в валюте котировки
                    )
            return ticker_data
        else:
            return {
                item["symbol"]: TickerDailyItem(
                    p=round(float(item["change24h"]) * 100, 2),  # Конвертируем в проценты
                    v=int(float(item["quoteVolume"]))  # Объем торгов в валюте котировки
                ) for item in raw_data["data"]
            }

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров Bitget в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсов (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "USDT".
        :return: Словарь с фьючерсными тикерами и их 24-часовой статистикой.
        """
        return BitgetAdapter.ticker_24h(raw_data=raw_data, only_usdt=only_usdt)

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
                tickers_info[data["symbol"]] = float(data["fundingRate"]) * 100
            return tickers_info
        elif isinstance(raw_data, dict):
            data = raw_data["data"][0]
            return {data["symbol"]: float(data["fundingRate"]) * 100}
        else:
            raise TypeError(f"Wrong raw_data type: {type(raw_data)}, excepted List[Dict] or Dict")

    @staticmethod
    def kline_message(raw_msg: Any) -> List[KlineDict]:
        """
        Преобразует сырое сообщение с вебсокета Bitget в унифицированный формат свечи (Kline).

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект Kline или список объектов Kline.
        :raises AdapterException: Если сообщение имеет неверную структуру или данные невозможно преобразовать.
        """
        try:
            symbol = raw_msg["arg"]["instId"]
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
                    v=float(data[6]),  # Quote volume (в USDT)
                    T=None,
                    x=None,
                    i=timeframe
                ))

            return klines
        except KeyError as e:
            raise AdapterException(f"Missing key in Bitget kline message: {e}")
        except (TypeError, ValueError) as e:
            raise AdapterException(f"Invalid data format in Bitget kline message: {e}")
