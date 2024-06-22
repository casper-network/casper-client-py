import dataclasses

from pycspr.api.node.sse.constants import DEFAULT_HOST
from pycspr.api.node.sse.constants import DEFAULT_PORT
from pycspr.api.node.sse.constants import DEFAULT_PORT_REST


@dataclasses.dataclass
class ConnectionInfo:
    """Encapsulates information required to connect to a node's SSE API.

    """
    # Host address.
    host: str = DEFAULT_HOST

    # Number of exposed speculative SSE port.
    port: int = DEFAULT_PORT

    @property
    def address(self) -> str:
        """Return address of remote SSE server.

        """
        return f"http://{self.host}:{self.port}/events"
