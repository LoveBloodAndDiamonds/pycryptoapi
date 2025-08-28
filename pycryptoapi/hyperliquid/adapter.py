from typing import Any, Dict, List

from ..abstract import AbstractAdapter
from ..types import TickerDailyItem, OpenInterestDict, KlineDict, AggTradeDict, DepthDict, LiquidationDict


class HyperliquidAdapter(AbstractAdapter):

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
        pass

    @staticmethod
    def futures_ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        pass

    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        pass

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        pass

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        pass
