"""Interact with the local API of La Marzocco machines."""

import asyncio
import logging
import signal
from typing import Any, Callable

import httpx
import websockets

from .const import WEBSOCKET_RETRY_DELAY
from .exceptions import AuthFail, RequestNotSuccessful

_logger = logging.getLogger(__name__)


class LaMarzoccoLocalClient:
    """Class to interact with machine via local API."""

    def __init__(
        self,
        host: str,
        local_bearer: str,
        local_port: int = 8081,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._host = host
        self._local_port = local_port
        self._local_bearer = local_bearer

        self.websocket_connected = False
        self.terminating: bool = False

        if client is None:
            self._client = httpx.AsyncClient()
        else:
            self._client = client

    @property
    def host(self) -> str:
        """Return the hostname of the machine."""
        return self._host

    async def get_config(self) -> dict[str, Any]:
        """Get current config of machine from local API."""
        headers = {"Authorization": f"Bearer {self._local_bearer}"}

        try:
            response = await self._client.get(
                f"http://{self._host}:{self._local_port}/api/v1/config", headers=headers
            )
        except httpx.RequestError as exc:
            raise RequestNotSuccessful(
                f"Requesting local API failed with exception: {exc}"
            ) from exc
        if response.is_success:
            return response.json()
        if response.status_code == 403:
            raise AuthFail("Local API returned 403.")
        raise RequestNotSuccessful(
            f"Querying local API failed with statuscode: {response.status_code}"
        )

    async def websocket_connect(
        self,
        callback: Callable[[str | bytes], None] | None = None,
        use_sigterm_handler: bool = True,
    ) -> None:
        """Connect to the websocket of the machine."""
        headers = {"Authorization": f"Bearer {self._local_bearer}"}
        async for websocket in websockets.connect(
            f"ws://{self._host}:{self._local_port}/api/v1/streaming",
            extra_headers=headers,
        ):
            try:
                if use_sigterm_handler:
                    # Close the connection when receiving SIGTERM.
                    loop = asyncio.get_running_loop()
                    loop.add_signal_handler(
                        signal.SIGTERM, loop.create_task, websocket.close()
                    )
                self.websocket_connected = True
                # Process messages received on the connection.
                async for message in websocket:
                    if self.terminating:
                        return
                    if callback is not None:
                        try:
                            callback(message)
                        except Exception as e:  # pylint: disable=broad-except
                            _logger.exception(
                                "Error during callback: %s", e, exc_info=True
                            )
            except websockets.ConnectionClosed:
                if self.terminating:
                    return
                _logger.debug(
                    "Websocket disconnected, reconnecting in %s", WEBSOCKET_RETRY_DELAY
                )
                await asyncio.sleep(WEBSOCKET_RETRY_DELAY)
                continue
            except websockets.WebSocketException as ex:
                _logger.warning("Exception during websocket connection: %s", ex)