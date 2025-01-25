from typing import Any, List

from ..abstract import AbstractAdapter


class MexcAdapter(AbstractAdapter):

    @staticmethod
    def process_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        if only_usdt:
            return [item for item in raw_data["data"] if item.endswith("USDT")]
        else:
            return raw_data["data"]

    @staticmethod
    def process_futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        if only_usdt:
            tickers: List[str] = []
            for item in raw_data["data"]:
                symbol: str = item["symbol"]
                if symbol.endswith("_USDT"):
                    tickers.append(symbol)
            return tickers
        else:
            return [item["symbol"] for item in raw_data["data"]]
