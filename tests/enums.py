# Примеры работы:
from pycryptoapi.enums import Exchange

# pair = Exchange.BINANCE + MarketType.SPOT
# print(pair)  # MarketPair.BINANCE_SPOT
# print(pair.split())  # (Exchange.BINANCE, MarketType.SPOT)

print(Exchange("BINANCE"))
print(type(Exchange("BINANCE")))
