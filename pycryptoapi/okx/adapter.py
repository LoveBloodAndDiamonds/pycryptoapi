from typing import Any, List

from ..abstract import AbstractAdapter


class OkxAdapter(AbstractAdapter):

    @staticmethod
    def process_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        if only_usdt:
            tickers: List[str] = []
            for item in raw_data["data"]:
                symbol: str = item["instId"]
                if symbol.endswith("-USDT"):
                    tickers.append(symbol)
            return tickers
        else:
            return [item["instId"] for item in raw_data["data"]]

    @staticmethod
    def process_futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        if only_usdt:
            tickers: List[str] = []
            for item in raw_data["data"]:
                symbol: str = item["instId"]
                if symbol.endswith("-USDT-SWAP"):
                    tickers.append(symbol)
            return tickers
        else:
            return [item["instId"] for item in raw_data["data"]]
