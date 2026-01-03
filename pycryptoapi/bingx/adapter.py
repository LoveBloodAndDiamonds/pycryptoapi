from typing import Any, Dict, List, Union

from ..abstract import AbstractAdapter
from ..exceptions import AdapterException
from ..types import (
    AggTradeDict,
    DepthDict,
    KlineDict,
    LiquidationDict,
    OpenInterestDict,
    OpenInterestItem,
    TickerDailyItem,
)


class BingxAdapter(AbstractAdapter):
    @staticmethod
    def tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        try:
            data = (
                raw_data.get("data", raw_data)
                if isinstance(raw_data, dict)
                else raw_data
            )
            if isinstance(data, dict) and "symbols" in data:
                items = data["symbols"]
            elif isinstance(data, list):
                items = data
            else:
                items = []
            if only_usdt:
                return [
                    item["symbol"] for item in items if item["symbol"].endswith("USDT")
                ]
            return [item["symbol"] for item in items]
        except Exception as e:
            raise AdapterException(f"Error adapting BingX tickers data: {e}")

    @staticmethod
    def futures_tickers(raw_data: Any, only_usdt: bool = True) -> List[str]:
        return BingxAdapter.tickers(raw_data, only_usdt)

    @staticmethod
    def ticker_24h(raw_data: Any, only_usdt: bool = True) -> Dict[str, TickerDailyItem]:
        try:
            data = (
                raw_data.get("data", raw_data)
                if isinstance(raw_data, dict)
                else raw_data
            )
            if not isinstance(data, list):
                return {}
            result: Dict[str, TickerDailyItem] = {}
            for item in data:
                symbol = item.get("symbol", "")
                if only_usdt and not symbol.endswith("USDT"):
                    continue
                percent_raw = item.get("priceChangePercent", 0)
                percent_str = str(percent_raw).strip()
                if percent_str.endswith("%"):
                    percent_str = percent_str[:-1]
                try:
                    percent = round(float(percent_str), 2)
                except ValueError:
                    percent = 0.0
                volume_raw = item.get("quoteVolume", item.get("volume", 0))
                result[symbol] = TickerDailyItem(
                    p=percent,
                    v=float(volume_raw),
                )
            return result
        except Exception as e:
            raise AdapterException(f"Error adapting BingX ticker 24h data: {e}")

    @staticmethod
    def futures_ticker_24h(
        raw_data: Any, only_usdt: bool = True
    ) -> Dict[str, TickerDailyItem]:
        return BingxAdapter.ticker_24h(raw_data, only_usdt)

    @staticmethod
    def funding_rate(raw_data: Any, **kwargs) -> Dict[str, float]:
        try:
            data = (
                raw_data.get("data", raw_data)
                if isinstance(raw_data, dict)
                else raw_data
            )
            items = data if isinstance(data, list) else [data]
            result: Dict[str, float] = {}
            for item in items:
                if not isinstance(item, dict):
                    continue
                symbol = item.get("symbol")
                rate = item.get("lastFundingRate", item.get("fundingRate"))
                if not symbol or rate in (None, ""):
                    continue
                result[symbol] = float(rate) * 100
            return result
        except Exception as e:
            raise AdapterException(f"Error adapting BingX funding rate data: {e}")

    @staticmethod
    def open_interest(
        raw_data: Union[Dict[str, Any], List[Dict[str, Any]]],
    ) -> OpenInterestDict:
        try:
            data = (
                raw_data.get("data", raw_data)
                if isinstance(raw_data, dict)
                else raw_data
            )
            items = data if isinstance(data, list) else [data]
            result: OpenInterestDict = {}
            for item in items:
                if not isinstance(item, dict):
                    continue
                symbol = item.get("symbol", "")
                time_val = item.get("time") or item.get("timestamp") or item.get("ts")
                open_interest = item.get("openInterest", item.get("openInterestValue"))
                if not symbol or open_interest in (None, ""):
                    continue
                result[symbol] = OpenInterestItem(
                    t=int(time_val) if time_val is not None else 0,
                    v=float(open_interest),
                )
            return result
        except Exception as e:
            raise AdapterException(f"Error adapting BingX open interest data: {e}")

    @staticmethod
    def kline(raw_data: Dict[str, Any]) -> List[KlineDict]:
        try:
            data = raw_data.get("data", raw_data)
            items = (
                data.get("klines")
                if isinstance(data, dict) and "klines" in data
                else data
            )
            symbol = raw_data.get("symbol") if isinstance(raw_data, dict) else ""
            if not symbol and isinstance(data, dict):
                symbol = data.get("symbol", "")

            if isinstance(items, list) and items and isinstance(items[0], dict):
                return [
                    KlineDict(
                        s=symbol,
                        t=int(kline["time"]),
                        o=float(kline["open"]),
                        h=float(kline["high"]),
                        l=float(kline["low"]),
                        c=float(kline["close"]),
                        v=float(kline["volume"]),
                        i=None,
                        T=None,
                        x=None,
                    )
                    for kline in sorted(items, key=lambda x: int(x["time"]))
                ]

            if isinstance(items, list):
                return [
                    KlineDict(
                        s=symbol,
                        t=int(kline[0]),
                        o=float(kline[1]),
                        h=float(kline[2]),
                        l=float(kline[3]),
                        c=float(kline[4]),
                        v=float(kline[5]),
                        i=None,
                        T=int(kline[6]) if len(kline) > 6 else None,
                        x=None,
                    )
                    for kline in sorted(items, key=lambda x: int(x[0]))
                ]
            return []
        except Exception as e:
            raise AdapterException(f"Error adapting BingX kline data: {e}")

    @staticmethod
    def futures_kline(raw_data: Dict[str, Any]) -> List[KlineDict]:
        return BingxAdapter.kline(raw_data)

    @staticmethod
    def kline_message(raw_msg: Any) -> List[KlineDict]:
        raise NotImplementedError()

    @staticmethod
    def aggtrades_message(raw_msg: Any) -> List[AggTradeDict]:
        try:
            trades = raw_msg.get("data", [])
            return [
                AggTradeDict(
                    t=int(trade["T"]),
                    s=str(trade["s"]),
                    S="SELL" if bool(trade["m"]) else "BUY",
                    p=float(trade["p"]),
                    v=float(trade["q"]),
                )
                for trade in sorted(trades, key=lambda x: int(x["T"]))
            ]
        except Exception as e:
            raise AdapterException(f"Error adapting BingX aggtrades message: {e}")

    @staticmethod
    def liquidation_message(raw_msg: Any) -> List[LiquidationDict]:
        raise NotImplementedError()

    @staticmethod
    def depth(raw_data: Any) -> DepthDict:
        try:
            data = (
                raw_data.get("data", raw_data)
                if isinstance(raw_data, dict)
                else raw_data
            )
            if not isinstance(data, dict):
                raise ValueError("depth data is not a dict")
            asks = data.get("asks") or data.get("a")
            bids = data.get("bids") or data.get("b")
            return AbstractAdapter._parse_and_sort_depth(asks, bids)
        except Exception as e:
            raise AdapterException(f"Error adapting BingX depth data: {e}")

    @staticmethod
    def futures_last_price(raw_data: Any) -> Dict[str, float]:
        try:
            data = (
                raw_data.get("data", raw_data)
                if isinstance(raw_data, dict)
                else raw_data
            )
            if isinstance(data, list):
                return {
                    item["symbol"]: float(item.get("lastPrice", item.get("price")))
                    for item in data
                }
            if isinstance(data, dict):
                symbol = data.get("symbol", "")
                if not symbol:
                    return {}
                return {symbol: float(data.get("lastPrice", data.get("price")))}
            return {}
        except Exception as e:
            raise AdapterException(f"Error adapting BingX last price data: {e}")
