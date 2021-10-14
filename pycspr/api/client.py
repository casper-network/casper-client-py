import time
import typing

from pycspr import factory
from pycspr import types
from pycspr.api import constants
from pycspr.api import endpoints
from pycspr.api import params as params_factory
from pycspr.api.connection import NodeConnection
from pycspr.api.constants import NodeEventChannelType
from pycspr.api.constants import NodeEventType



class NodeClient():
    """Exposes a set of (categorised) functions for interacting  with a node.
    
    """
    def __init__(self, connection: NodeConnection):
        """Instance constructor.

        :param connection: Information required to connect to a node.
        
        """
        self.connection = connection


    def get_account_balance(
        self,
        purse_uref: typing.Union[str, types.UnforgeableReference],
        state_root_hash: typing.Union[bytes, None] = None
    ) -> int:
        """Returns account balance at a certain global state root hash.

        :param purse_uref: URef of a purse associated with an on-chain account.
        :param state_root_hash: A node's root state hash at some point in chain time, if none then defaults to the most recent.
        :returns: Account balance if on-chain account is found.

        """
        state_root_hash = state_root_hash or self.get_state_root_hash()
        params = params_factory.get_account_balance_params(purse_uref, state_root_hash)
        response = self.connection.get_rpc_response(constants.RPC_STATE_GET_BALANCE, params)

        return int(response["balance_value"])


    def get_account_info(self, account_key: typing.Union[bytes, str], block_id: types.OptionalBlockIdentifer = None) -> dict:
        """Returns account information at a certain global state root hash.

        :param account_key: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """
        params = params_factory.get_account_info_params(account_key, block_id)
        response = self.connection.get_rpc_response(constants.RPC_STATE_GET_ACCOUNT_INFO, params)

        return response["account"]


    def get_account_main_purse_uref(self, account_key: typing.Union[bytes, str], block_id: types.OptionalBlockIdentifer = None) -> types.UnforgeableReference:
        """Returns an on-chain account's main purse unforgeable reference.

        :param account_key: Key of an on-chain account.
        :param block_id: Identifier of a finalised block.
        :returns: Account main purse unforgeable reference.

        """
        account_info = self.get_account_info(account_key, block_id)
    
        return factory.create_uref_from_string(account_info["main_purse"])


    def get_account_named_key(self, account_key: typing.Union[bytes, str], key_name: str, block_id: types.OptionalBlockIdentifer = None) -> str:
        """Returns a named key stored under an account.

        :param account_key: An account holder's public key prefixed with a key type identifier.
        :param key_name: Name of key under which account data is stored.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """
        account_info = self.get_account_info(account_key, block_id)
        named_keys = [i for i in account_info["named_keys"] if i["name"] == key_name]

        return None if len(named_keys) == 0 else named_keys[0]["key"]


    def get_auction_info(self, block_id: types.OptionalBlockIdentifer = None) -> dict:
        """Returns current auction system contract information.

        :returns: Current auction system contract information.

        """
        params = params_factory.get_auction_info_params(block_id)
        response = self.connection.get_rpc_response(constants.RPC_STATE_GET_AUCTION_INFO, params)

        return response


    def get_block(self, block_id: types.OptionalBlockIdentifer = None) -> dict:
        """Returns on-chain block information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block information.

        """
        params = params_factory.get_block_params(block_id)
        response = self.connection.get_rpc_response(constants.RPC_CHAIN_GET_BLOCK, params)

        return response["block"]


    def get_block_at_era_switch(
        self,
        polling_interval_seconds: float = 1.0,
        max_polling_time_seconds: float = 120.0
    ) -> dict:
        """Returns last finalised block in current era.

        :param polling_interval_seconds: Time interval time (in seconds) before polling for next switch block.
        :param max_polling_time_seconds: Maximum time in seconds to poll.
        :returns: On-chain block information.

        """
        elapsed = 0.0
        while True:
            block = get_block(node)
            if block["header"]["era_end"] is not None:
                return block

            elapsed += polling_interval_seconds
            if elapsed > max_polling_time_seconds:
                break
            time.sleep(polling_interval_seconds)

        return endpoints.get_block_at_era_switch.execute(
            self.connection,
            polling_interval_seconds,
            max_polling_time_seconds
            )


    def get_block_transfers(self, block_id: types.OptionalBlockIdentifer = None) -> typing.Tuple[str, list]:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :returns: On-chain block transfers information.

        """
        params = params_factory.get_block_transfers_params(block_id)
        response = self.connection.get_rpc_response(constants.RPC_CHAIN_GET_BLOCK_TRANSFERS, params)

        return (response["block_hash"], response["transfers"])


    def get_deploy(self, deploy_id: typing.Union[bytes, str]) -> dict:
        """Returns on-chain deploy information.

        :param deploy_id: Identifier of a finalised block.
        :returns: On-chain deploy information.

        """
        params = params_factory.get_deploy_params(deploy_id)
        response = self.connection.get_rpc_response(constants.RPC_INFO_GET_DEPLOY, params)

        return response


    def get_dictionary_item(self, identifier: types.DictionaryIdentifier) -> dict:
        """Returns on-chain data stored under a dictionary item.

        :param identifier: Identifier required to query a dictionary item.
        :returns: On-chain data stored under a dictionary item.

        """
        params = params_factory.get_dictionary_item_params(identifier)
        response = self.connection.get_rpc_response(constants.RPC_STATE_GET_DICTIONARY_ITEM, params)

        return response


    def get_era_info(self, block_id: types.OptionalBlockIdentifer = None) -> dict:
        """Returns current era information.

        :param block_id: Identifier of a finalised block.
        :returns: Era information.

        """
        params = params_factory.get_era_info_params(block_id)
        response = self.connection.get_rpc_response(constants.RPC_CHAIN_GET_ERA_INFO_BY_SWITCH_BLOCK, params)

        return response["era_summary"]


    def get_events(
        self,
        callback: typing.Callable,
        channel_type: NodeEventChannelType,
        event_type: NodeEventType = None,
        event_id: int = 0
    ):
        """Binds to a node's event stream - events are passed to callback for processing.

        :param callback: Callback to invoke whenever an event of relevant type is received.
        :param channel_type: Type of event channel to which to bind.
        :param event_type: Type of event type to listen for (all if unspecified).
        :param event_id: Identifer of event from which to start stream listening.

        """
        endpoints.get_events.execute(self.connection, callback, channel_type, event_type, event_id)


    def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        return endpoints.get_node_metrics.execute(self.connection)


    def get_node_metric(self, metric_id: str) -> list:
        """Returns node metrics information filtered by a particular metric.

        :param metric_id: Identifier of node metric.
        :returns: Node metrics information filtered by a particular metric.

        """
        return endpoints.get_node_metrics.execute(self.connection, metric_id)


    def get_node_peers(self) -> dict:
        """Returns node peers information.

        :returns: Node peers information.

        """
        return endpoints.get_node_peers.execute(self.connection)


    def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return endpoints.get_node_status.execute(self.connection)


    def get_rpc_endpoint(self, endpoint: str) -> dict:
        """Returns RPC schema.

        :param endpoint: A specific endpoint of interest.
        :returns: A JSON-RPC schema endpoint fragment.

        """
        return endpoints.get_rpc_endpoint.execute(self.connection, endpoint)


    def get_rpc_endpoints(self) -> typing.Union[dict, list]:
        """Returns RPC schema.

        :returns: A list of all supported JSON-RPC endpoints.

        """
        return endpoints.get_rpc_endpoints.execute(self.connection)


    def get_rpc_schema(self) -> dict:
        """Returns RPC schema.

        :returns: Node JSON-RPC API schema.

        """
        return endpoints.get_rpc_schema.execute(self.connection)


    def get_state_item(
        self,
        item_key: str,
        item_path: typing.Union[str, typing.List[str]] = [],
        state_root_hash: typing.Union[bytes, None] = None
        ) -> bytes:
        """Returns a representation of an item stored under a key in global state.

        :param item_key: Storage item key.
        :param item_path: Storage item path.
        :param state_root_hash: A node's root state hash at some point in chain time, if none then defaults to the most recent.
        :returns: Item stored under passed key/path.

        """
        item_path = item_path if isinstance(item_path, list) else [item_path]
        state_root_hash = state_root_hash or self.get_state_root_hash()
        
        return endpoints.get_state_item.execute(self.connection, item_key, item_path, state_root_hash)


    def get_state_root_hash(self, block_id: types.OptionalBlockIdentifer = None) -> bytes:
        """Returns an root hash of global state at a specified block.

        :param block_id: Identifier of a finalised block.
        :returns: State root hash at specified block.

        """
        return bytes.fromhex(
            endpoints.get_state_root_hash.execute(self.connection, block_id)
        )


    def get_validator_changes(self) -> dict:
        """Returns status changes of active validators.

        :param node: Information required to connect to a node.
        :returns: Status changes of active validators.

        """
        return endpoints.get_validator_changes.execute(self.connection)


    def send_deploy(self, deploy: types.Deploy):
        """Dispatches a deploy to a node for processing.

        :param deploy: A deploy to be processed at a node.

        """
        return endpoints.put_deploy.execute(self.connection, deploy)
