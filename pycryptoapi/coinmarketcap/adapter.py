from typing import Any, Dict


class CoinmarketcapAdapter:
    """
    Адаптер для преобразования сырых данных Coinmarketcap в унифицированный вид.
    """

    @staticmethod
    def cryptocurrency_map(raw_data: Any) -> Dict[str, int]:
        """Преобразует сырые данные из запроса в словарь: {ticker: rank}"""
        return {el["symbol"]: el["rank"] for el in raw_data["data"]}
