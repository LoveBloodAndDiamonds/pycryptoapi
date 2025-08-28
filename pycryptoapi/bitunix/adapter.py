from datetime import datetime, timezone
from typing import Any, Dict, List

from ..abstract import AbstractAdapter
from ..exceptions import AdapterException
from ..types import TickerDailyItem, OpenInterestDict, KlineDict, AggTradeDict, DepthDict, LiquidationDict


class BitunixAdapter(AbstractAdapter):

    @staticmethod
    def futures_last_price(raw_data: Any) -> Any:
        raise NotImplementedError()

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
    def futures_kline(raw_data: Dict[str, Any]) -> List[KlineDict]:
        raise NotImplementedError()

    @staticmethod
    def kline(raw_data: Dict[str, Any]) -> List[KlineDict]:
        raise NotImplementedError()

    @staticmethod
    def open_interest(raw_data: Dict[str, Any]) -> OpenInterestDict:
        raise NotImplementedError()

    @staticmethod
    def funding_rate(raw_data: Any, **kwargs) -> Dict[str, float]:
        raise NotImplementedError()

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        try:
            return [
                AggTradeDict(
                    t=int(
                        datetime.fromisoformat(trade["t"].replace("Z", "+00:00"))
                        .replace(tzinfo=timezone.utc)
                        .timestamp() * 1000
                    ),
                    s=raw_msg["symbol"],
                    p=float(trade["p"]),
                    v=float(trade["v"]),
                    S="SELL" if trade["s"] == "sell" else "BUY",
                ) for trade in raw_msg["data"]
            ]
        except Exception as e:
            raise AdapterException(e) from e

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        if only_usdt:
            res = {}
            for item in raw_data["data"]:
                symbol = item["symbol"]
                if symbol.endswith("USDT"):
                    res[symbol] = TickerDailyItem(
                        p=round((float(item["last"]) / float(item["open"]) - 1) * 100, 2),
                        v=float(item["quoteVol"])
                    )
        else:
            res = {}
            for item in raw_data["data"]:
                res[item["symbol"]] = TickerDailyItem(
                    p=round((float(item["last"]) / float(item["open"]) - 1) * 100, 2),
                    v=float(item["quoteVol"])
                )
        return res

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        raise NotImplementedError()

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        if only_usdt:
            return [item["symbol"] for item in raw_data["data"] if item["symbol"].endswith("USDT")]
        else:
            return [item["symbol"] for item in raw_data["data"]]

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        raise NotImplementedError()
