__all__ = ["CLIENTS_MAPPER", "SOCKETS_MAPPER", "ADAPTERS_MAPPER"]

from typing import Dict, Type

from .abstract import AbstractAdapter, AbstractClient, AbstractSocketManager
from .binance import BinanceAdapter, BinanceClient, BinanceSocketManager
from .bingx import BingxAdapter, BingxClient, BingxSocketManager
from .bitget import BitgetAdapter, BitgetClient, BitgetSocketManager
from .bitunix import BitunixAdapter, BitunixClient, BitunixSocketManager
from .bybit import BybitAdapter, BybitClient, BybitSocketManager
from .enums import Exchange
from .gate import GateAdapter, GateClient, GateSocketManager
from .hyperliquid import HyperliquidAdapter, HyperliquidClient, HyperliquidSocketManager
from .kcex import KcexAdapter, KcexClient, KcexSocketManager
from .mexc import MexcAdapter, MexcClient, MexcSocketManager
from .okx import OkxAdapter, OkxClient, OkxSocketManager
from .xt import XtAdapter, XtClient, XtSocketManager

# Маппинг клиентов бирж
CLIENTS_MAPPER: Dict[Exchange, Type[AbstractClient]] = {
    Exchange.BINANCE: BinanceClient,
    Exchange.BITGET: BitgetClient,
    Exchange.BYBIT: BybitClient,
    Exchange.MEXC: MexcClient,
    Exchange.OKX: OkxClient,
    Exchange.GATE: GateClient,
    Exchange.XT: XtClient,
    Exchange.BITUNIX: BitunixClient,
    Exchange.KCEX: KcexClient,
    Exchange.HYPERLIQUID: HyperliquidClient,
    Exchange.BINGX: BingxClient,
}

# Маппинг менеджеров сокетов бирж
SOCKETS_MAPPER: Dict[Exchange, Type[AbstractSocketManager]] = {
    Exchange.BINANCE: BinanceSocketManager,
    Exchange.BITGET: BitgetSocketManager,
    Exchange.BYBIT: BybitSocketManager,
    Exchange.MEXC: MexcSocketManager,
    Exchange.OKX: OkxSocketManager,
    Exchange.GATE: GateSocketManager,
    Exchange.XT: XtSocketManager,
    Exchange.BITUNIX: BitunixSocketManager,
    Exchange.KCEX: KcexSocketManager,
    Exchange.HYPERLIQUID: HyperliquidSocketManager,
    Exchange.BINGX: BingxSocketManager,
}

# Маппинг адаптеров бирж
ADAPTERS_MAPPER: Dict[Exchange, Type[AbstractAdapter]] = {
    Exchange.BINANCE: BinanceAdapter,
    Exchange.BITGET: BitgetAdapter,
    Exchange.BYBIT: BybitAdapter,
    Exchange.MEXC: MexcAdapter,
    Exchange.OKX: OkxAdapter,
    Exchange.GATE: GateAdapter,
    Exchange.XT: XtAdapter,
    Exchange.BITUNIX: BitunixAdapter,
    Exchange.KCEX: KcexAdapter,
    Exchange.HYPERLIQUID: HyperliquidAdapter,
    Exchange.BINGX: BingxAdapter,
}
