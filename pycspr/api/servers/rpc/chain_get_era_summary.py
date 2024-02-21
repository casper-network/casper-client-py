from pycspr.types import BlockID
from pycspr.api import constants
from pycspr.api.servers.rpc import utils
from pycspr.api.servers.rpc.utils import Proxy


def exec(proxy: Proxy, block_id: BlockID = None) -> dict:
    """Returns consensus era summary information.

    :param proxy: Remote RPC server proxy. 
    :param block_id: Identifier of a block.
    :returns: Era summary information.

    """
    params: dict = utils.get_block_id(block_id, False)
    response: dict = proxy.get_response(constants.RPC_CHAIN_GET_ERA_SUMMARY, params)

    return response["era_summary"]
