__all__ = ["CLIENTS_MAPPER", "SOCKETS_MAPPER", "ADAPTERS_MAPPER"]

from typing import Dict, Type

from .abstract import AbstractClient, AbstractAdapter, AbstractSocketManager
from .binance import BinanceClient, BinanceAdapter, BinanceSocketManager
from .bitget import BitgetClient, BitgetAdapter, BitgetSocketManager
from .bybit import BybitClient, BybitAdapter, BybitSocketManager
from .enums import Exchange
from .gate import GateSocketManager, GateClient, GateAdapter
from .mexc import MexcClient, MexcAdapter, MexcSocketManager
from .okx import OkxClient, OkxAdapter, OkxSocketManager
from .xt import XtClient, XtAdapter, XtSocketManager
from .bitunix import BitunixClient, BitunixAdapter, BitunixSocketManager
from .kcex import KcexAdapter, KcexClient, KcexSocketManager

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
}
