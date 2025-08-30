import asyncio
from datetime import datetime
from pycryptoapi.kcex import KcexSocketManager, KcexAdapter
from pycryptoapi.enums import MarketType
from pycryptoapi.types import AggTradeDict
from pycryptoapi.fixes import init_kcex_perpetual_fix, kcex_perpetual_aggtrade_fix


current_candle = None  # словарь с текущей свечой
current_minute = None  # "ключ" для текущей минуты


def floor_minute(ts: int) -> datetime:
    """Приводим время trade (мс) к минуте."""
    return datetime.fromtimestamp(ts / 1000).replace(second=0, microsecond=0)


def new_candle(symbol: str, minute: datetime, trade: AggTradeDict) -> dict:
    """Создать новую свечу из первого трейда."""
    return {
        "symbol": symbol,
        "minute": minute,
        "open": trade["p"],
        "high": trade["p"],
        "low": trade["p"],
        "close": trade["p"],
        "volume": trade["v"],
    }


async def callback(msg):
    global current_candle, current_minute

    msg = kcex_perpetual_aggtrade_fix(msg)

    try:
        trades: list[AggTradeDict] = KcexAdapter.aggtrades_message(msg)
    except:
        return

    for trade in trades:
        minute = floor_minute(trade["t"])

        if current_minute is None:
            # Первая свеча
            current_minute = minute
            current_candle = new_candle(trade["s"], minute, trade)
            continue

        if minute != current_minute:
            # Минутка сменилась → печатаем старую свечу и начинаем новую
            print(
                f"[{current_candle['minute'].strftime('%H:%M')}] "
                f"O={current_candle['open']} "
                f"H={current_candle['high']} "
                f"L={current_candle['low']} "
                f"C={current_candle['close']} "
                f"V={current_candle['volume']}"
            )

            current_minute = minute
            current_candle = new_candle(trade["s"], minute, trade)
        else:
            # Обновляем текущую свечу
            price = trade["p"]
            current_candle["high"] = max(current_candle["high"], price)
            current_candle["low"] = min(current_candle["low"], price)
            current_candle["close"] = price
            current_candle["volume"] += trade["v"]


async def main():
    socket = KcexSocketManager.aggtrades_socket(
        market_type=MarketType.FUTURES,
        tickers=["TRX_USDT"],
        callback=callback,
    )
    await init_kcex_perpetual_fix()
    await socket.start()


if __name__ == "__main__":
    asyncio.run(main())

    '''
TRX: 0.33811
514 / 1 738

    
ours / real
btc: 1 / 1000
eth: 1 / 1000
trx: 1 / 10
    '''

# "cs": 10,


'''

Request URL
https://www.kcex.com/fapi/v1/contract/detailV2?client=web
Request Method
GET
'''