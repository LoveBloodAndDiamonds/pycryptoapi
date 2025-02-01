import logging
from typing import Dict, Any, Literal, Optional
from typing import List

import aiohttp
import loguru
from loguru._logger import Logger  # noqa

from ..abstract import BaseClient


class CoinmarketcapClient(BaseClient):
    """Клиент для работы с Coinmarketcap.com"""

    _BASE_URL: str = "https://pro-api.coinmarketcap.com"

    def __init__(
            self,
            session: aiohttp.ClientSession,
            api_key: str,
            logger: logging.Logger | Logger = loguru.logger,
    ) -> None:
        super().__init__(session=session, logger=logger)

        self._api_key: str = api_key

    async def cryptocurrency_map(
            self,
            sort: Literal["id", "cmc_rank"] = "cmc_rank",
            symbol: Optional[str] = None,
            aux: Optional[str] = "platform,first_historical_data,last_historical_data,is_active",  # Read more in docs
            listing_status: Literal["active", "inactive", "untracked"] = "active",
            start: int = 1,
            limit: int = 5000,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMap"""
        return await self._make_request(
            method="GET",
            url=self._BASE_URL + "/v1/cryptocurrency/map",
            params=self.filter_params({
                "sort": sort,
                "symbol": symbol,
                "aux": aux,
                "listing_status": listing_status,
                "start": start,
                "limit": limit,
            }),
            headers={
                "Accepts": "application/json",
                "X-CMC_PRO_API_KEY": self._api_key
            }
        )
