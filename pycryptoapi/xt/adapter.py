__all__ = ["XtAdapter", ]

from typing import Any, List, Dict, Union

from ..abstract import AbstractAdapter
from ..exceptions import AdapterException
from ..types import TickerDailyItem, KlineDict, AggTradeDict, LiquidationDict, OpenInterestDict, \
    DepthDict


class XtAdapter(AbstractAdapter):

    @staticmethod
    def tickers(raw_data: Dict[str, Any], only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные тикеров в список символов.

        :param raw_data: Сырые данные тикеров (список словарей).
        :param only_usdt: Если True, возвращаются только тикеры, оканчивающиеся на 'USDT'.
        :return: Список тикеров.
        """
        if only_usdt:
            tickers = []
            for item in raw_data["result"]:
                symbol = item["s"]
                if symbol.endswith("_usdt"):
                    tickers.append(symbol)
            return tickers
        else:
            return [item["s"] for item in raw_data["result"]]

    @staticmethod
    def futures_tickers(raw_data: Dict[str, Any], only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные фьючерсных тикеров в список символов.

        :param raw_data: Сырые данные фьючерсных тикеров (список словарей).
        :param only_usdt: Если True, возвращаются только тикеры, оканчивающиеся на 'USDT'.
        :return: Список фьючерсных тикеров.
        """
        return XtAdapter.tickers(raw_data, only_usdt)

    @staticmethod
    def ticker_24h(raw_data: Dict[str, Any], only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров в унифицированный вид.

        :param raw_data: Сырые данные статистики (список словарей).
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Словарь с тикерами и их статистикой за 24 часа.
        """
        if only_usdt:
            tickers_data = {}
            for item in raw_data["result"]:
                symbol = item["s"]
                if symbol.endswith("_usdt"):
                    tickers_data[symbol] = TickerDailyItem(
                        p=round(float(item["cr"]) * 100, 2),
                        v=float(item["v"]),
                    )
            return tickers_data
        else:
            return {
                item["s"]: TickerDailyItem(
                    p=round(float(item["cr"]) * 100, 2),
                    v=float(item["v"]),
                ) for item in raw_data["result"]
            }

    @staticmethod
    def futures_ticker_24h(raw_data: Dict[str, Any], only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсов (список словарей).
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Словарь с фьючерсными тикерами и их статистикой за 24 часа.
        """
        if only_usdt:
            tickers_data = {}
            for item in raw_data["result"]:
                symbol = item["s"]
                if symbol.endswith("_usdt"):
                    tickers_data[symbol] = TickerDailyItem(
                        p=round(float(item["r"]) * 100, 2),
                        v=float(item["v"]),
                    )
            return tickers_data
        else:
            return {
                item["s"]: TickerDailyItem(
                    p=round(float(item["r"]) * 100, 2),
                    v=float(item["v"]),
                ) for item in raw_data["result"]
            }

    @staticmethod
    def funding_rate(raw_data: List[Dict[str, str]], only_usdt: bool = True) -> Dict[str, float]:
        raise NotImplementedError("Not implemented yet...")

    @staticmethod
    def open_interest(raw_data: Union[Dict[str, str], List[Dict[str, str]]]) -> OpenInterestDict:
        raise NotImplementedError("Not implemented yet...")

    @staticmethod
    def kline(raw_data: List[Any]) -> List[KlineDict]:
        raise NotImplementedError("Not implemented yet...")

    @staticmethod
    def futures_kline(raw_data: List[Any]) -> List[KlineDict]:
        raise NotImplementedError("Not implemented yet...")

    @staticmethod
    def kline_message(raw_msg: Dict[str, Any]) -> List[KlineDict]:
        raise NotImplementedError("Not implemented yet...")

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        """
        Преобразует сырое сообщение с вебсокета Binance в унифицированный вид.

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект AggTradeDict или None, если сообщение невалидно.
        """
        try:
            data = raw_msg["data"]

            if "m" in data:  # futures
                return [
                    AggTradeDict(
                        t=data["t"],
                        s=data["s"],
                        S="BUY" if data["m"] == "BID" else "SELL",
                        p=float(data["p"]),
                        v=float(data["a"]),
                    )
                ]

            else:  # spot
                return [
                    AggTradeDict(
                        t=data["t"],
                        s=data["s"],
                        S="SELL" if data["b"] else "BUY",
                        p=float(data["p"]),
                        v=float(data["q"]),
                    )
                ]

        except (KeyError, ValueError, TypeError) as e:
            raise AdapterException(f"Invalid data format in Xt aggtrades message: {e}")

    @staticmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        raise NotImplementedError("Not implemented yet...")

    @staticmethod
    def depth(raw_data: Any) -> DepthDict:
        raise NotImplementedError("Not implemented yet...")
