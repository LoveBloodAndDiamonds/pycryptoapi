from typing import Optional, Union, List

from ..abstract import AbstractWebsocket, AbstractSocketManager


class HyperliquidWebsocket(AbstractWebsocket):

    @property
    def _subscribe_message(self) -> Optional[Union[str, List[str]]]:
        pass

    @property
    def _ping_message(self) -> Optional[str]:
        pass

    @property
    def _connection_uri(self) -> str:
        pass


class HyperliquidSocketManager(AbstractSocketManager):

    @classmethod
    def liquidations_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        raise NotImplementedError()

    @classmethod
    def tickers_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        raise NotImplementedError()

    @classmethod
    def aggtrades_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        pass

    @classmethod
    def klines_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        raise NotImplementedError()
