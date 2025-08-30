__all__ = ["init_fixes", "okx_perpetual_ticker_daily_fix", "okx_perpetual_aggtrade_fix",
           "mexc_perpetual_ticker_daily_fix", "mexc_perpetual_open_interest_fix", "mexc_perpetual_aggtrade_fix",
           "xt_perpetual_aggtrade_fix", "kcex_perpetual_aggtrade_fix", "init_kcex_perpetual_fix",
           "kcex_perpetual_open_interest_fix", ]

from pycryptoapi.enums import Exchange, MarketType
from .kcex_perpetual_fix import kcex_perpetual_aggtrade_fix, init_kcex_perpetual_fix, kcex_perpetual_open_interest_fix
from .mexc_perpetual_fix import init_mexc_perpetual_fix, mexc_perpetual_ticker_daily_fix, \
    mexc_perpetual_open_interest_fix, mexc_perpetual_aggtrade_fix
from .okx_perpetual_fix import okx_perpetual_aggtrade_fix, init_okx_perpetual_fix, okx_perpetual_ticker_daily_fix
from .xt_perpetual_fix import xt_perpetual_aggtrade_fix, init_xt_perpetual_fix


async def init_fixes(exchange: Exchange | list[Exchange], market_type: MarketType | list[MarketType]):
    """
    Инициализация различных объектов, которые помогают фиксить рыночные данные, которые возвращаются
    с запросов от некоторых бирж.

    Например контракты или прочее дерьмо, которые ублюдки на OKX и MEXC и KCEX и XT
    решили внедрить в свои фьючерсы, которые руинят объемы.
    """
    if isinstance(exchange, Exchange):
        exchange = [exchange]
    if isinstance(market_type, MarketType):
        market_type = [market_type]

    for e in exchange:
        for m in market_type:
            if e == Exchange.OKX and m == MarketType.FUTURES:
                await init_okx_perpetual_fix()
            if e == Exchange.MEXC and m == MarketType.FUTURES:
                await init_mexc_perpetual_fix()
            if e == Exchange.XT and m == MarketType.FUTURES:
                await init_xt_perpetual_fix()
            if e == Exchange.KCEX and m == MarketType.FUTURES:
                await init_kcex_perpetual_fix()
