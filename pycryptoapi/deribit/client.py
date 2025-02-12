__all__ = ["DeribitClient"]

import time
from typing import Optional, Dict, Any

import aiohttp


class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/"

    def __init__(self, api_key: str, api_secret: str) -> None:
        super().__init__()

        self._client_id: str = api_key
        self._client_secret: str = api_secret
        self._token: Optional[str] = None
        self._token_expiry: float = 0

    async def _authenticate(self) -> None:
        """Authenticate and get access token using client credentials."""
        if self._token is None or time.time() >= self._token_expiry:
            async with aiohttp.ClientSession() as session:
                params = {
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "grant_type": "client_credentials"
                }

                async with session.get(f"{self.BASE_URL}public/auth", params=params) as response:
                    data = await response.json()

                    if "error" in data:
                        raise Exception(f"Authentication error: {data['error']}")

                    self.token = data["result"]["access_token"]
                    # Обновляем токен за минуту до истечения
                    self.token_expiry = time.time() + data["result"]["expires_in"] - 60

    async def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a request to the Deribit API."""
        await self._authenticate()

        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),  # Генерация уникального ID
            "method": method,
            "params": params or {}
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.BASE_URL, headers=headers, json=payload) as response:
                data = await response.json()
                return data

    async def get_price(self, instrument_name: str) -> Dict[str, Any]:
        """Example method to get the current price of an instrument."""
        return await self._send_request("public/ticker", {"instrument_name": instrument_name})

    async def get_orderbook(self, instrument_name: str, depth: Optional[int] = 10) -> Dict[str, Any]:
        """  https://docs.deribit.com/?shell#public-get_order_book """
        return await self._send_request(
            "/public/get_order_book",
            {
                "instrument_name": instrument_name,
                "depth": depth
            }
        )

    async def get_instrument(self, instrument_name: str) -> Dict[str, Any]:
        """ https://docs.deribit.com/#public-get_index_price_names """
        return await self._send_request(
            "/public/get_instrument",
            {
                "instrument_name": instrument_name
            }
        )

    async def get_instruments(self, currency: str, kind: str = "option") -> Dict[str, Any]:
        """ https://docs.deribit.com/?shell#public-get_instruments """
        return await self._send_request(
            "/public/get_instruments",
            {
                "currency": currency,
                "king": kind
            }
        )

    async def ticker(self, instrument_name: str) -> Dict[str, Any]:
        """  https://docs.deribit.com/#public-ticker """
        return await self._send_request(
            "/public/ticker",
            {
                "instrument_name": instrument_name
            }
        )

    async def buy(
            self,
            # label: str = ""
            # amount: float,
            # valid_until
            instrument_name: str,
            contracts: float,
            price: float,
            post_only: bool = True,
            time_in_force: str = "good_til_cancelled",
            type: str = "limit",  # noqa

    ) -> Dict[str, Any]:
        """ https://docs.deribit.com/#private-buy """
        return await self._send_request(
            "/private/buy",
            {
                "instrument_name": instrument_name,
                "contracts": contracts,
                "price": price,
                "post_only": post_only,
                "time_in_force": time_in_force,
                "type": type,
            }
        )

    async def cancel(self, order_id: str) -> Dict[str, Any]:
        """ https://docs.deribit.com/#private-cancel """
        return await self._send_request(
            "/private/cancel",
            {
                "order_id": order_id
            }
        )

    async def sell(
            self,
            instrument_name: str,
            contracts: float,
            price: float,
            type: str = "limit",  # noqa
            time_in_force: str = "good_til_cancelled",
            reduce_only: bool = True,
    ) -> Dict[str, Any]:
        """ https://docs.deribit.com/#private-sell """
        return await self._send_request(
            "/private/sell",
            {
                "instrument_name": instrument_name,
                "contracts": contracts,
                "price": price,
                "type": type,
                "time_in_force": time_in_force,
                "reduce_only": reduce_only,
            }
        )

    async def edit(self, order_id: str, price: float, contracts: float, **kwargs) -> Dict[str, Any]:
        """ https://docs.deribit.com/#private-edit """
        return await self._send_request(
            "/private/edit",
            {
                "order_id": order_id,
                "price": price,
                "contracts": contracts,
                **kwargs
            }
        )

    async def get_order_state(self, order_id: str) -> Dict[str, Any]:
        """ https://docs.deribit.com/#private-get_order_state """
        return await self._send_request(
            "/private/get_order_state",
            {
                "order_id": order_id
            }
        )

    async def get_user_trades_by_currency(self, currency: str, kind: str = "option", **kwargs) -> Dict[str, Any]:
        """ https://docs.deribit.com/#private-get_user_trades_by_currency """
        return await self._send_request(
            "/private/get_user_trades_by_currency",
            {
                "currency": currency,
                "kind": kind,
                **kwargs
            }
        )

    async def close_position(self, instrument_name: str, price: float, type: str = "limit") -> Dict[str, Any]:  # noqa
        """ https://docs.deribit.com/#private-close_position """
        return await self._send_request(
            "/close_position",
            {
                "instrument_name": instrument_name,
                "price": price,
                "type": type,
            }
        )
