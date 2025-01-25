from typing import Any, List

from ..abstract import AbstractAdapter


class BybitAdapter(AbstractAdapter):

    @staticmethod
    def process_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        if only_usdt:
            tickers: List[str] = []
            for item in raw_data["result"]["list"]:
                symbol: str = item["symbol"]
                if symbol.endswith("USDT"):
                    tickers.append(symbol)
            return tickers
        else:
            return [item["symbol"] for item in raw_data["result"]["list"]]

    @staticmethod
    def process_futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        return BybitAdapter.process_tickers(raw_data, only_usdt)
