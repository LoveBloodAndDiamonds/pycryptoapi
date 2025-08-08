from typing import Any, List, Dict, Union

from ..abstract import AbstractAdapter
from ..exceptions import AdapterException
from ..types import TickerDailyItem, OpenInterestItem, KlineDict, AggTradeDict, LiquidationDict, OpenInterestDict, \
    DepthDict


class BinanceAdapter(AbstractAdapter):

    @staticmethod
    def tickers(raw_data: List[Dict[str, str]], only_usdt: bool = True) -> List[str]:
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
    def futures_tickers(raw_data: List[Dict[str, str]], only_usdt: bool = True) -> List[str]:
        """
        Преобразует сырые данные фьючерсных тикеров в список символов.

        :param raw_data: Сырые данные фьючерсных тикеров (список словарей).
        :param only_usdt: Если True, возвращаются только тикеры, оканчивающиеся на 'USDT'.
        :return: Список фьючерсных тикеров.
        """
        return BinanceAdapter.tickers(raw_data, only_usdt)

    @staticmethod
    def ticker_24h(raw_data: List[Dict[str, str]], only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для тикеров в унифицированный вид.

        :param raw_data: Сырые данные статистики (список словарей).
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Словарь с тикерами и их статистикой за 24 часа.
        """
        if only_usdt:
            tickers_data = {}
            for item in raw_data:
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers_data[symbol] = TickerDailyItem(
                        p=round(float(item["priceChangePercent"]), 2),
                        v=int(float(item["quoteVolume"])),
                    )
            return tickers_data
        else:
            return {
                item["symbol"]: TickerDailyItem(
                    p=round(float(item["priceChangePercent"]), 2),
                    v=int(float(item["quoteVolume"])),
                ) for item in raw_data
            }

    @staticmethod
    def futures_ticker_24h(raw_data: List[Dict[str, str]], only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсов (список словарей).
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Словарь с фьючерсными тикерами и их статистикой за 24 часа.
        """
        return BinanceAdapter.ticker_24h(raw_data, only_usdt)

    @staticmethod
    def funding_rate(raw_data: List[Dict[str, str]], only_usdt: bool = True) -> Dict[str, float]:
        """
        Преобразует сырые данные ставки финансирования для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные ставки финансирования фьючерсов (список словарей)
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Cловарь с фьючерсными тикерами и их ставкой финансирования.
        """
        if only_usdt:
            tickers_data = {}
            for item in raw_data:
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers_data[symbol] = float(item["lastFundingRate"]) * 100
            return tickers_data
        else:
            return {item["symbol"]: float(item["lastFundingRate"]) for item in raw_data}

    @staticmethod
    def open_interest(raw_data: Union[Dict[str, str], List[Dict[str, str]]]) -> OpenInterestDict:
        """
        Преобразует сырые данные открытого интереса в унифицированный вид.

        :param raw_data: Сырые данные открытого интереса по тикеру. Можно передать список данных.
        :return: Cловарь с фьючерсными тикерами и их открытым интересом.
        """
        # {'openInterest': '84548.990', 'symbol': 'BTCUSDT', 'time': 1738480839502}
        if isinstance(raw_data, dict):
            return {raw_data["symbol"]: OpenInterestItem(
                t=int(raw_data["time"]),
                v=float(raw_data["openInterest"]))}
        elif isinstance(raw_data, list):
            result = {}
            for item in raw_data:
                result[item["symbol"]] = OpenInterestItem(t=int(item["time"]), v=float(item["openInterest"]))
            return result
        else:
            raise ValueError(f"Wrong raw_data type: {type(raw_data)}, excepted: list or dict")

    @staticmethod
    def kline(raw_data: List[Any]) -> List[KlineDict]:
        """
        Преобразует сырой ответ с запроса Binance в унифицированный формат свечи (Kline).
        """
        return [
            KlineDict(
                s="",
                t=k[0],
                o=float(k[1]),
                h=float(k[2]),
                l=float(k[3]),
                c=float(k[4]),
                v=float(k[7]),
                i=None,
                T=None,
                x=None,
            )
            for k in raw_data
        ]

    @staticmethod
    def futures_kline(raw_data: List[Any]) -> List[KlineDict]:
        """
        Преобразует сырой ответ с запроса Binance в унифицированный формат свечи (Kline).
        """
        return BinanceAdapter.kline(raw_data)

    @staticmethod
    def kline_message(raw_msg: Dict[str, Any]) -> List[KlineDict]:
        """
        Преобразует сырое сообщение с вебсокета Binance в унифицированный формат свечи (Kline).

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект Kline.
        :raises AdapterException: Если сообщение имеет неверную структуру или данные невозможно преобразовать.
        """
        try:
            try:
                kline = raw_msg["data"]["k"]
            except KeyError:
                kline = raw_msg["k"]
            return [KlineDict(
                s=kline["s"],
                t=kline["t"],
                o=float(kline["o"]),
                h=float(kline["h"]),
                l=float(kline["l"]),
                c=float(kline["c"]),
                v=float(kline["q"]),  # Используем quote volume (в USDT)
                T=kline["T"],
                x=kline["x"],  # Берём через .get(), чтобы не выбрасывало KeyError
                i=kline["i"]
            )]
        except KeyError as e:
            raise AdapterException(f"Missing key in Binance kline message: {e}")
        except (TypeError, ValueError) as e:
            raise AdapterException(f"Invalid data format in Binance kline message: {e}")

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        """
        Преобразует сырое сообщение с вебсокета Binance в унифицированный вид.

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект AggTradeDict или None, если сообщение невалидно.
        """
        try:
            # Если сообщение в обёртке (мульти-стрим), то достаем `data`
            if "data" in raw_msg:
                raw_msg = raw_msg["data"]

            return [AggTradeDict(
                t=raw_msg["T"],
                s=raw_msg["s"],
                S="SELL" if raw_msg["m"] else "BUY",
                p=float(raw_msg["p"]),
                v=float(raw_msg["q"])
            )]

        except (KeyError, ValueError, TypeError) as e:
            raise AdapterException(f"Invalid data format in Binance aggtrades message: {e}")

    @staticmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        raise NotImplementedError("Not implemented yet...")

    @staticmethod
    def depth(raw_data: Any) -> DepthDict:
        try:
            return AbstractAdapter._parse_and_sort_depth(raw_data["asks"], raw_data["bids"])
        except Exception as e:
            raise AdapterException(f"BybitAdapter error: {e}")

    @staticmethod
    def futures_last_price(raw_data: Any) -> Dict[str, float]:
        return {item["symbol"]: float(item["lastPrice"]) for item in raw_data}
