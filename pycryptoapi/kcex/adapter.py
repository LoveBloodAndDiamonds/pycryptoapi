from typing import Any, List, Dict

from ..abstract import AbstractAdapter
from ..exceptions import AdapterException
from ..types import TickerDailyItem, OpenInterestDict, KlineDict, AggTradeDict, LiquidationDict, DepthDict


class KcexAdapter(AbstractAdapter):
    @staticmethod
    def futures_last_price(raw_data: Any) -> Any:
        return {item["symbol"]: item["lastPrice"] for item in raw_data["data"]}

    @staticmethod
    def depth(raw_data: Any) -> DepthDict:
        raise NotImplementedError()

    @staticmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        raise NotImplementedError()

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        try:
            return [
                AggTradeDict(
                    t=data["t"],
                    s=raw_msg["symbol"],
                    S="SELL" if data["M"] else "BUY",
                    p=data["p"],
                    v=data["v"],
                ) for data in raw_msg["data"]
            ]
        except Exception as e:
            raise AdapterException(e)

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
        try:
            return {item["symbol"]: item["holdVol"] * item["lastPrice"] for item in raw_data["data"]}  # wrong, this is contrcts i think
        except Exception as e:
            raise AdapterException(e)

    @staticmethod
    def funding_rate(raw_data: Any, **kwargs) -> Dict[str, float]:
        try:
            return {item["symbol"]: item["fundingRate"] * 100 for item in raw_data["data"]}
        except Exception as e:
            raise AdapterException(e)

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        try:
            if only_usdt:
                result = {}
                for item in raw_data["data"]:
                    if item["symbol"].endswith("USDT"):
                        result[item["symbol"]] = TickerDailyItem(
                            p=round(item["riseFallRate"] * 100, 2),
                            v=item["amount24"]
                        )
            else:
                result = {}
            return result
        except Exception as e:
            raise AdapterException(e)

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        raise NotImplementedError()

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        if only_usdt:
            return [item["symbol"] for item in raw_data["data"] if item["symbol"].endswith("USDT")]
        return [item["symbol"] for item in raw_data["data"]]

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        raise NotImplementedError()
