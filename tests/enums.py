# Примеры работы:

from pycryptoapi.enums import Exchange, Timeframe

# pair = Exchange.BINANCE + MarketType.SPOT
# print(pair)  # MarketCombo.BINANCE_SPOT
# print(pair.split())  # (Exchange.BINANCE, MarketType.SPOT)

print(Exchange("BINANCE"))
print(type(Exchange("BINANCE")))

print(Timeframe.MIN_1.to_exchange_format(exchange=Exchange.MEXC))
