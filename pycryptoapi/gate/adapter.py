__all__ = ["GateAdapter", ]

from typing import Any, List, Dict

from ..abstract import AbstractAdapter
from ..exceptions import AdapterException
from ..types import TickerDailyItem, KlineDict, AggTradeDict, LiquidationDict, OpenInterestDict, DepthDict


class GateAdapter(AbstractAdapter):
    """
    Адаптер для преобразования сырых данных MEXC в унифицированный вид.
    """

    @staticmethod
    def futures_kline(raw_data: Dict[str, Any]) -> List[KlineDict]:
        raise NotImplementedError()

    @staticmethod
    def kline(raw_data: Dict[str, Any]) -> List[KlineDict]:
        raise NotImplementedError()

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные тикеров Gate в список символов.

        :param raw_data: Сырые данные тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только тикеры, оканчивающиеся на "USDT".
        :return: Список символов тикеров.
        """
        if only_usdt:
            tickers = []
            for item in raw_data:
                symbol = item["currency_pair"]
                if symbol.endswith("USDT"):
                    tickers.append(symbol)
            return tickers
        return [item["currency_pair"] for item in raw_data]

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
            for item in raw_data:
                symbol = item["contract"]
                if symbol.endswith("_USDT"):
                    tickers.append(symbol)
            return tickers
        return [item["contract"] for item in raw_data]

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров Gate в унифицированный вид.

        :param raw_data: Сырые данные статистики (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "USDT".
        :return: Словарь с тикерами и их 24-часовой статистикой.
        """
        if only_usdt:
            ticker_data = {}
            for item in raw_data:
                symbol = item["currency_pair"]
                if not symbol.endswith("USDT"):
                    continue

                ticker_data[symbol] = TickerDailyItem(
                    p=float(item["change_percentage"]),  # Конвертируем в проценты
                    v=float(item["quote_volume"])  # Объём торгов в валюте котировки
                )
            return ticker_data
        else:
            return {
                item["currency_pair"]: TickerDailyItem(
                    p=float(item["change_percentage"]),  # Конвертируем в проценты
                    v=float(item["quote_volume"])  # Объём торгов в валюте котировки
                ) for item in raw_data
            }

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров Gate в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсных тикеров (словарь с ключом "data").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "_USDT".
        :return: Словарь с фьючерсными тикерами и их 24-часовой статистикой.
        """
        if only_usdt:
            ticker_data = {}
            for item in raw_data:
                symbol = item["contract"]
                if not symbol.endswith("_USDT"):
                    continue
                ticker_data[symbol] = TickerDailyItem(
                    p=float(item["change_percentage"]),  # Процентное изменение
                    v=int(float(item["volume_24h_quote"]))  # КОНТРАКТЫ
                )
            return ticker_data
        else:
            ticker_data = {}
            for item in raw_data:
                symbol = item["contract"]
                ticker_data[symbol] = TickerDailyItem(
                    p=float(item["change_percentage"]),  # Процентное изменение
                    v=int(float(item["volume_24h_quote"]))  # КОНТРАКТЫ
                )
            return ticker_data

    @staticmethod
    def funding_rate(raw_data: Dict[str, Any], only_usdt: bool = True) -> Dict[str, float]:
        """
        Преобразует сырые данные ставки финансирования для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные ставки финансирования фьючерсов.
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Cловарь с фьючерсными тикерами и их ставкой финансирования.
        """
        raise NotImplementedError()

    @staticmethod
    def kline_message(raw_msg: Any) -> List[KlineDict]:
        """
        Преобразует сырое сообщение с вебсокета Gate (спот или фьючерсы) в унифицированный формат свечи (Kline).

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект Kline или список объектов Kline.
        :raises AdapterException: Если сообщение имеет неверную структуру или данные невозможно преобразовать.
        """
        raise NotImplementedError()

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        """
        Преобразует сырое сообщение с вебсокета MEXC в унифицированный вид.

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Список унифицированных объектов AggTradeDict или None, если сообщение невалидно.
        :raises: AdapterException, если возникла ошибка при обработке данных.
        """
        try:
            channel = raw_msg.get("channel")
            if channel == "futures.trades":
                return [
                    AggTradeDict(
                        t=item["create_time_ms"],
                        s=item["contract"].replace("_", ""),
                        S="BUY" if item["size"] >= 0 else "SELL",
                        p=float(item["price"]),
                        v=abs(item["size"]),
                    ) for item in raw_msg["result"]
                ]
            elif channel == "spot.trades":
                item = raw_msg["result"]
                return [
                    AggTradeDict(
                        t=int(float(item["create_time_ms"])),
                        s=item["currency_pair"].replace("_", ""),
                        S=item["side"].upper(),
                        p=float(item["price"]),
                        v=item["amount"],
                    )
                ]
            raise AdapterException("Unknown format")
        except (KeyError, ValueError, TypeError) as e:
            raise AdapterException(f"Error processing Gate aggTrade({raw_msg}): {e}")

    @staticmethod
    def open_interest(raw_data: Dict[str, Any], only_usdt: bool = True) -> OpenInterestDict:
        """
        Преобразует сырые данные открытого интереса для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные открытого интереса.
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Cловарь с тикерами и их ставкой финансирования.
        """
        raise NotImplementedError()

    @staticmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        raise NotImplementedError("Not implemented yet...")

    @staticmethod
    def depth(raw_data: Any) -> DepthDict:
        try:
            return AbstractAdapter._parse_and_sort_depth(raw_data["asks"], raw_data["bids"])
        except Exception as e:
            raise AdapterException(f"BybitAdapter error: {e}")
