import time
from typing import Any, Dict, List

from ..abstract import AbstractAdapter
from ..types import TickerDailyItem, OpenInterestDict, KlineDict, AggTradeDict, DepthDict, LiquidationDict
from ..exceptions import AdapterException


class HyperliquidAdapter(AbstractAdapter):

    @staticmethod
    def futures_last_price(raw_data: Any) -> Any:
        """
        Возвращает последнюю цену по фьючерсам.
        raw_data = data[1] из metaAndAssetCtxs (список метрик).
        """
        try:
            return {i: float(item["markPx"]) for i, item in enumerate(raw_data)}
        except Exception as e:
            raise AdapterException(f"Error adapting futures last price: {e}")

    @staticmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        raise NotImplementedError()

    @staticmethod
    def depth(raw_data: Any) -> DepthDict:
        raise NotImplementedError()

    @staticmethod
    def kline_message(raw_msg: Any) -> List[KlineDict]:
        raise NotImplementedError()

    @staticmethod
    def futures_kline(raw_data: Any) -> List[KlineDict]:
        raise NotImplementedError()

    @staticmethod
    def kline(raw_data: Any) -> List[KlineDict]:
        raise NotImplementedError()

    @staticmethod
    def open_interest(raw_data: Any) -> OpenInterestDict:
        """
        Возвращает словарь: {symbol: {"t": timestamp, "v": oi}}
        """
        try:
            universe = raw_data[0]["universe"]
            stats = raw_data[1]

            return {
                asset["name"]: {"t": int(time.time()), "v": float(stat["openInterest"])}
                for asset, stat in zip(universe, stats)
            }
        except Exception as e:
            raise AdapterException(f"Error adapting open interest: {e}")

    @staticmethod
    def funding_rate(raw_data: Any, **kwargs) -> Dict[str, float]:
        raise NotImplementedError()

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        raise NotImplementedError()

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        """
        Возвращает словарь вида:
        { "BTC": {"p": ..., "v": ...}, "ETH": {...}, ... }
        где p — изменение цены % за 24ч, v — дневной объём
        """
        try:
            universe = raw_data[0]["universe"]
            stats = raw_data[1]

            result: Dict[str, TickerDailyItem] = {}
            for asset, stat in zip(universe, stats):
                name = asset["name"]
                mark = float(stat["markPx"])
                prev = float(stat["prevDayPx"])
                p = ((mark - prev) / prev) * 100 if prev != 0 else 0.0
                v = float(stat["dayNtlVlm"])
                result[name] = {"p": round(p, 2), "v": round(v, 2)}

            return result
        except Exception as e:
            raise AdapterException(f"Error adapting futures tickers 24h: {e}")

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        pass

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        try:
            return [item["name"] for item in raw_data[0]["universe"]]
        except Exception as e:
            raise AdapterException(f"Error adapting futures tickers: {e}")

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        raise NotImplementedError()
