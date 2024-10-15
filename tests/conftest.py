"""Test configuration."""

from __future__ import annotations

from contextlib import closing
from functools import partial
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socket import SOCK_STREAM
from socket import socket
from socketserver import TCPServer
from threading import Thread
from time import sleep
from typing import Callable
from typing import Iterator
from typing import cast
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

import pytest


def get_unused_tcp_port() -> int:
    """Get an unused TCP port on the local host.

    Returns:
        The port number.
    """
    with closing(socket(type=SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return cast(int, sock.getsockname()[1])


HTTPServerFactory = Callable[[Path], str]


@pytest.fixture
def http_server_factory() -> Iterator[HTTPServerFactory]:
    """A pytest fixture for a local HTTP server factory.

    Yields:
        The HTTP server factory.
    """
    server_host = "127.0.0.1"
    server_disposers: list[Callable[[], None]] = []

    def create(directory: Path) -> str:
        server_port = get_unused_tcp_port()
        server = TCPServer(
            (server_host, server_port),
            partial(SimpleHTTPRequestHandler, directory=str(directory)),
        )
        server_disposers.append(server.shutdown)
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        server_url = f"http://{server_host}:{server_port}"

        # Wait until the server has booted.
        request = Request(server_url, method="HEAD")
        while True:
            try:
                with urlopen(request):
                    pass
            except URLError as exc:
                if isinstance(exc.reason, ConnectionRefusedError):
                    sleep(0.1)
                else:
                    raise
            else:
                break

        return server_url

    yield create

    while server_disposers:
        dispose = server_disposers.pop()
        dispose()
