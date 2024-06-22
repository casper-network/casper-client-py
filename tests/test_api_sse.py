from pycspr import NodeEventChannel
from pycspr import NodeEventInfo
from pycspr import NodeEventType
from pycspr import NodeRpcClient
from pycspr import NodeSseClient


async def test_await_n_blocks(NODE_SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 2
    current = await RPC_CLIENT.get_block_height()
    future = current + offset
    await NODE_SSE_CLIENT.await_n_blocks(offset)
    assert await RPC_CLIENT.get_block_height() == future


async def test_await_n_eras(NODE_SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 1
    current = await RPC_CLIENT.get_era_height()
    future = current + offset
    await NODE_SSE_CLIENT.await_n_eras(offset)
    assert await RPC_CLIENT.get_era_height() == future


async def test_await_n_events(NODE_SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 1
    current = await RPC_CLIENT.get_block_height()
    future = current + offset
    await NODE_SSE_CLIENT.await_n_events(offset, NodeEventChannel.main, NodeEventType.BlockAdded)
    assert await RPC_CLIENT.get_block_height() == future


async def test_await_until_block_n(NODE_SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 2
    future = await RPC_CLIENT.get_block_height() + offset
    await NODE_SSE_CLIENT.await_until_block_n(future)
    assert await RPC_CLIENT.get_block_height() == future


async def test_await_until_era_n(NODE_SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 1
    future = await RPC_CLIENT.get_era_height() + offset
    await NODE_SSE_CLIENT.await_until_era_n(future)
    assert await RPC_CLIENT.get_era_height() == future


async def test_get_events(NODE_SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    def ecallback(einfo: NodeEventInfo):
        assert isinstance(einfo, NodeEventInfo)
        raise InterruptedError()

    try:
        NODE_SSE_CLIENT.get_events(ecallback, NodeEventChannel.main, NodeEventType.BlockAdded)
    except InterruptedError:
        pass
    else:
        raise ValueError("Event capture error")


async def test_yield_events(NODE_SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    for einfo in NODE_SSE_CLIENT.yield_events(NodeEventChannel.main, NodeEventType.BlockAdded):
        assert isinstance(einfo, NodeEventInfo)
        break
