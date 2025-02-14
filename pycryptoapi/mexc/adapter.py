from typing import Any, List, Dict

from ..abstract import AbstractAdapter
from ..exc import AdapterException
from ..types import TickerDailyItem, KlineDict, OpenInterestItem, AggTradeDict


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
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
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

                ticker_data[symbol] = TickerDailyItem(
                    p=round(float(item["priceChangePercent"]) * 100, 2),  # Конвертируем в проценты
                    v=int(float(item["quoteVolume"]))  # Объём торгов в валюте котировки
                )
            return ticker_data
        else:
            return {
                item["symbol"]: TickerDailyItem(
                    p=round(float(item["priceChangePercent"]) * 100, 2),  # Конвертируем в проценты
                    v=int(float(item["quoteVolume"]))  # Объём торгов в валюте котировки
                ) for item in raw_data
            }

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
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
                ticker_data[symbol] = TickerDailyItem(
                    p=round(price_change, 2),  # Процентное изменение
                    v=int(float(item["volume24"]))
                )
            return ticker_data
        else:
            ticker_data = {}
            for item in raw_data["data"]:
                symbol = item["symbol"]
                avg_price = (float(item["high24Price"]) + float(item["lower24Price"])) / 2
                price_change = ((float(item["lastPrice"]) - avg_price) / avg_price) * 100 if avg_price != 0 else 0
                ticker_data[symbol] = TickerDailyItem(
                    p=round(price_change, 2),  # Процентное изменение
                    v=int(float(item["volume24"]))
                )
            return ticker_data

    @staticmethod
    def funding_rate(raw_data: Dict[str, Any], only_usdt: bool = True) -> Dict[str, float]:
        """
        Преобразует сырые данные ставки финансирования для фьючерсных тикеров в унифицированный вид.

        :param raw_data: Сырые данные ставки финансирования фьючерсов (список словарей)
        :param only_usdt: Если True, возвращаются данные только для тикеров, оканчивающихся на 'USDT'.
        :return: Cловарь с фьючерсными тикерами и их ставкой финансирования.
        """
        if only_usdt:
            tickers_info = {}
            for item in raw_data["data"]:
                symbol = item["symbol"]
                if symbol.endswith("_USDT"):
                    tickers_info[symbol] = float(item["fundingRate"]) * 100
            return tickers_info
        else:
            return {item["symbol"]: float(item["fundingRate"]) * 100 for item in raw_data["data"]}

    @staticmethod
    def kline_message(raw_msg: Any) -> List[KlineDict]:
        """
        Преобразует сырое сообщение с вебсокета MEXC (спот или фьючерсы) в унифицированный формат свечи (Kline).

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Унифицированный объект Kline или список объектов Kline.
        :raises AdapterException: Если сообщение имеет неверную структуру или данные невозможно преобразовать.
        """
        try:
            # Обработка спота
            if "d" in raw_msg and "k" in raw_msg["d"]:
                data = raw_msg["d"]["k"]
                return [KlineDict(
                    s=raw_msg["s"],
                    t=int(data["t"]),
                    o=float(data["o"]),
                    h=float(data["h"]),
                    l=float(data["l"]),
                    c=float(data["c"]),
                    v=float(data["v"]),
                    T=int(data["T"]),
                    x=None,
                    i=data["i"]
                )]

            # Обработка фьючерсов
            elif "symbol" in raw_msg and "data" in raw_msg:
                data = raw_msg["data"]
                return [KlineDict(
                    s=data["symbol"].replace("_", ""),
                    t=int(data["t"]),
                    o=float(data["o"]),
                    h=float(data["h"]),
                    l=float(data["l"]),
                    c=float(data["c"]),
                    v=float(data["a"]),
                    T=None,  # Добавляем 60 сек, так как таймфрейм 1 мин
                    x=None,
                    i=data["interval"]
                )]

            raise AdapterException("Unsupported message format or missing data.")
        except KeyError as e:
            raise AdapterException(f"Missing key in MEXC kline message: {e}")
        except (TypeError, ValueError) as e:
            raise AdapterException(f"Invalid data format in MEXC kline message: {e}")

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        """
        Преобразует сырое сообщение с вебсокета MEXC в унифицированный вид.

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Список унифицированных объектов AggTradeDict или None, если сообщение невалидно.
        :raises: AdapterException, если возникла ошибка при обработке данных.
        """
        try:
            # Проверяем первый формат (spot@public.deals.v3.api)
            if isinstance(raw_msg, dict) and "d" in raw_msg and "deals" in raw_msg["d"]:
                trades = raw_msg["d"]["deals"]

                return [
                    {
                        "s": raw_msg["s"],  # Символ
                        "t": int(trade["t"]),
                        "p": float(trade["p"]),
                        "v": float(trade["v"]),
                    }
                    for trade in trades
                ]

            # Проверяем второй формат (push.deal)
            if isinstance(raw_msg, dict) and "symbol" in raw_msg and "data" in raw_msg:
                trade = raw_msg["data"]
                return [
                    {
                        "s": raw_msg["symbol"].replace("_", ""),  # Приводим BTC_USDT → BTCUSDT
                        "t": int(trade["t"]),
                        "p": float(trade["p"]),
                        "v": float(trade["v"]),
                    }
                ]

            raise AdapterException("Unknown format")
        except (KeyError, ValueError, TypeError) as e:
            raise AdapterException(f"Error processing MEXC aggTrade({raw_msg}): {e}")

    @staticmethod
    def open_interest(raw_data: Dict[str, Any]) -> Dict[str, OpenInterestItem]:
        raise NotImplementedError("Not implemented yet...")
