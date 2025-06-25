from typing import Any, List, Dict

from ..abstract import AbstractAdapter
from ..exceptions import AdapterException
from ..types import TickerDailyItem, KlineDict, OpenInterestItem, AggTradeDict, LiquidationDict, OpenInterestDict


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
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
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
                    ticker_data[symbol] = TickerDailyItem(
                        p=round(float(item["price24hPcnt"]) * 100, 2),  # Изменение цены в процентах за 24ч
                        v=int(float(item["turnover24h"]))  # Объем за 24ч в USDT. Объем в монетах - volume24h
                    )
            return ticker_data
        else:
            return {
                item["symbol"]: TickerDailyItem(
                    p=round(float(item["price24hPcnt"]) * 100, 2),  # Изменение цены в процентах за 24ч
                    v=int(float(item["turnover24h"]))  # Объем за 24ч в USDT. Объем в монетах - volume24h
                ) for item in raw_data["result"]
            }

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Преобразует сырые данные 24-часовой статистики для фьючерсных тикеров Bybit в унифицированный вид.

        :param raw_data: Сырые данные статистики фьючерсных тикеров (словарь с ключом "result").
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "USDT".
        :return: Словарь с фьючерсными тикерами и их 24-часовой статистикой.
        """
        return BybitAdapter.ticker_24h(raw_data, only_usdt)

    @staticmethod
    def funding_rate(raw_data: Dict[str, Dict[str, Any]], only_usdt: bool = True) -> Dict[str, float]:
        """
        Преобразует сырые данные ставки финансирования для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные ставки финансирования фьючерсов (список словарей)
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Cловарь с фьючерсными тикерами и их ставкой финансирования.
        """
        if only_usdt:
            tickers_info = {}
            for item in raw_data["result"]["list"]:
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers_info[symbol] = float(item["fundingRate"]) * 100
            return tickers_info
        else:
            return {item["symbol"]: float(item["fundingRate"]) * 100 for item in raw_data["result"]["list"]}

    @staticmethod
    def kline_message(raw_msg: Any) -> List[KlineDict]:
        """
        Преобразует сырое сообщение с вебсокета Bybit в унифицированный формат свечи (Kline).

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект Kline.
        :raises AdapterException: Если сообщение имеет неверную структуру или данные невозможно преобразовать.
        """
        try:
            data = raw_msg["data"][0]
            return [KlineDict(
                s=raw_msg["topic"].split(".")[-1],
                t=data["start"],
                o=float(data["open"]),
                h=float(data["high"]),
                l=float(data["low"]),
                c=float(data["close"]),
                v=float(data["turnover"]),  # Используем оборот (turnover) в USDT
                T=data["end"],
                x=data["confirm"],  # Флаг закрытия свечи
                i=data["interval"]  # Таймфрейм в минутах
            )]
        except KeyError as e:
            raise AdapterException(f"Missing key in Bybit kline message: {e}")
        except (TypeError, ValueError) as e:
            raise AdapterException(f"Invalid data format in Bybit kline message: {e}")

    @staticmethod
    def open_interest(raw_data: Dict[str, Any]) -> OpenInterestDict:
        # Обработка данных от Bybit
        try:
            result: dict[str, OpenInterestItem] = {}
            time: int = raw_data["time"]
            for item in raw_data["result"]["list"]:
                result[item["symbol"]] = OpenInterestItem(
                    t=time,
                    v=float(item["openInterest"])  # Открытый интерес
                )
            return result
        except KeyError as e:
            raise AdapterException(f"Missing key in Bybit open intrest data: {e}")
        except (TypeError, ValueError) as e:
            raise AdapterException(f"Invalid data format in Bybit open intrest data: {e}")

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        """
        Преобразует сырое сообщение с вебсокета Bybit в унифицированный вид.

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект AggTradeDict или None, если сообщение невалидно.
        """
        try:
            trades = raw_msg["data"]

            return [
                AggTradeDict(
                    t=trade["T"],
                    s=trade["s"],
                    S=trade["S"].upper(),
                    p=float(trade["p"]),
                    v=float(trade["v"])
                ) for trade in trades
            ]

        except (KeyError, ValueError, TypeError) as e:
            raise AdapterException(f"Error processing Bybit aggTrade({raw_msg}): {e}")

    @staticmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        """
        Преобразует сырое сообщение с вебсокета в унифицированный вид.
        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект LiquidationDict, или None, если сообщение невалидно.
        """
        try:
            liquidations = raw_msg["data"]

            return [
                LiquidationDict(
                    t=liquidation["T"],
                    s=liquidation["s"],
                    S=liquidation["S"].upper(),
                    v=float(liquidation["v"]),
                    p=float(liquidation["p"])
                )
                for liquidation in liquidations]
        except (KeyError, ValueError, TypeError) as e:
            raise AdapterException(f"Error processing Bybit liquidation({raw_msg}): {e}")

    @staticmethod
    def kline(raw_data: Dict[str, Any]) -> List[KlineDict]:
        """
        Преобразует сырой ответ с HTTP запроса в унифицированный вид.

        :param raw_data: Сырые данные с HTTP запроса klines
        :return: Список унифицированных свечей.
        """
        result = raw_data["result"]
        return [KlineDict(
            s=result["symbol"],
            t=int(item[0]),
            o=float(item[1]),
            h=float(item[2]),
            l=float(item[3]),
            c=float(item[4]),
            v=float(item[5]),
            i=None,
            T=None,
            x=None,
        ) for item in result["list"]]

    @staticmethod
    def futures_kline(raw_data: Dict[str, Any]) -> List[KlineDict]:
        """
        Преобразует сырой ответ с HTTP запроса в унифицированный вид.

        :param raw_data: Сырые данные с HTTP запроса klines
        :return: Список унифицированных свечей.
        """
        return BybitAdapter.kline(raw_data)
