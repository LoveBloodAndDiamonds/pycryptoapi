from typing import Any, List, Dict, Union

from ..abstract import AbstractAdapter
from ..exceptions import AdapterException
from ..types import TickerDailyItem, KlineDict, OpenInterestItem, AggTradeDict, LiquidationDict, OpenInterestDict


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
    def open_interest(raw_data: Union[Dict[str, Any], List[Dict[str, Any]]],
                      only_usdt: bool = True) -> OpenInterestDict:
        """
        Преобразует сырой ответ с запроса в унифированный формат.

        :param raw_data: Сырые данные открытого интереса по тикеру. Можно передать список данных.
        :param only_usdt: Если True, возвращает только данные для тикеров, оканчивающихся на "USDT".
        :return: Cловарь с фьючерсными тикерами и их открытым интересом.
        """
        # {'code': '00000',
        #     'data': [{'askPr': '108821.1',
        #        'askSz': '11.0513',
        #        'baseVolume': '141491.5099',
        #        'bidPr': '108821',
        #        'bidSz': '1.4616',
        #        'change24h': '0.00746',
        #        'changeUtc24h': '0.0144',
        #        'deliveryStartTime': None,
        #        'deliveryStatus': '',
        #        'deliveryTime': None,
        #        'fundingRate': '0.000023',
        #        'high24h': '109966',
        #        'holdingAmount': '49203.8842',
        #        'indexPrice': '108872.714460795874789',
        #        'lastPr': '108821',
        #        'low24h': '106741.3',
        #        'markPrice': '108821',
        #        'open24h': '108015.5',
        #        'openUtc': '107275.7',
        #        'quoteVolume': '15361104773.27924',
        #        'symbol': 'BTCUSDT',
        #        'ts': '1748089641516',
        #        'usdtVolume': '15361104773.27924'},
        #         { ... }
        #  }
        try:
            result: dict[str, OpenInterestItem] = {}
            if only_usdt:
                for i in raw_data["data"]:
                    symbol = i["symbol"]
                    if symbol.endswith("USDT"):
                        result[symbol] = OpenInterestItem(
                            t=int(i["ts"]),
                            v=float(i["holdingAmount"])
                        )
            else:
                return {i["symbol"]: OpenInterestItem(
                    t=int(i["ts"]),
                    v=float(i["holdingAmount"])
                ) for i in raw_data["data"]}
            return result
        except Exception as e:
            raise AdapterException(f"Error adapting bitget open interest data: {e}")

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

            return [
                KlineDict(
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
                ) for data in raw_msg["data"]
            ]

        except KeyError as e:
            raise AdapterException(f"Missing key in Bitget kline message: {e}")
        except (TypeError, ValueError) as e:
            raise AdapterException(f"Invalid data format in Bitget kline message: {e}")

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        """
        Преобразует сырое сообщение с вебсокета Bitget в унифицированный вид.

        :param raw_msg: Сырое сообщение с вебсокета.
        :return: Список унифицированных объектов AggTradeDict или None, если сообщение невалидно.
        :raises: AdapterException, если возникла ошибка при обработке данных.
        """
        try:
            trades = raw_msg["data"]

            symbol = raw_msg["arg"]["instId"]  # Получаем символ из аргументов запроса

            return [
                AggTradeDict(
                    t=int(trade["ts"]),
                    s=symbol,
                    S=trade["side"].upper(),
                    p=float(trade["price"]),
                    v=float(trade["size"])
                ) for trade in trades
            ]

        except (KeyError, ValueError, TypeError) as e:
            raise AdapterException(f"Error processing Bitget aggTrade ({raw_msg}): {e}")

    @staticmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        raise NotImplementedError("Not implemented yet...")
