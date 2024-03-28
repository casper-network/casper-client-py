import typing

from pycspr.factory import create_public_key_from_account_key
from pycspr.serializer.json.cl_value import decode as decode_cl_value
from pycspr.types.crypto import Digest
from pycspr.types.crypto import MerkleProofBytes
from pycspr.types.crypto import PublicKeyBytes
from pycspr.types.crypto import SignatureBytes
from pycspr.types.node.rpc import Address
from pycspr.types.node.rpc import AccountInfo
from pycspr.types.node.rpc import AccountKey
from pycspr.types.node.rpc import ActionThresholds
from pycspr.types.node.rpc import AssociatedKey
from pycspr.types.node.rpc import AuctionBidByDelegator
from pycspr.types.node.rpc import AuctionBidByValidator
from pycspr.types.node.rpc import AuctionBidByValidatorInfo
from pycspr.types.node.rpc import AuctionState
from pycspr.types.node.rpc import Block
from pycspr.types.node.rpc import BlockBody
from pycspr.types.node.rpc import BlockHeader
from pycspr.types.node.rpc import BlockHeight
from pycspr.types.node.rpc import BlockSignature
from pycspr.types.node.rpc import BlockTransfers
from pycspr.types.node.rpc import ContractVersion
from pycspr.types.node.rpc import Deploy
from pycspr.types.node.rpc import DeployApproval
from pycspr.types.node.rpc import DeployArgument
from pycspr.types.node.rpc import DeployExecutionInfo
from pycspr.types.node.rpc import DeployExecutableItem
from pycspr.types.node.rpc import DeployHeader
from pycspr.types.node.rpc import DeployOfModuleBytes
from pycspr.types.node.rpc import DeployOfStoredContractByHash
from pycspr.types.node.rpc import DeployOfStoredContractByHashVersioned
from pycspr.types.node.rpc import DeployOfStoredContractByName
from pycspr.types.node.rpc import DeployOfStoredContractByNameVersioned
from pycspr.types.node.rpc import DeployOfTransfer
from pycspr.types.node.rpc import DeployTimeToLive
from pycspr.types.node.rpc import EraID
from pycspr.types.node.rpc import EraInfo
from pycspr.types.node.rpc import EraSummary
from pycspr.types.node.rpc import EraValidators
from pycspr.types.node.rpc import EraValidatorWeight
from pycspr.types.node.rpc import Gas
from pycspr.types.node.rpc import GasPrice
from pycspr.types.node.rpc import Motes
from pycspr.types.node.rpc import NamedKey
from pycspr.types.node.rpc import NodeStatus
from pycspr.types.node.rpc import ProtocolVersion
from pycspr.types.node.rpc import SeigniorageAllocation
from pycspr.types.node.rpc import SeigniorageAllocationForDelegator
from pycspr.types.node.rpc import SeigniorageAllocationForValidator
from pycspr.types.node.rpc import Transfer
from pycspr.types.node.rpc import Timestamp
from pycspr.types.node.rpc import URef
from pycspr.types.node.rpc import URefAccessRights
from pycspr.types.node.rpc import ValidatorChanges
from pycspr.types.node.rpc import ValidatorStatusChange
from pycspr.types.node.rpc import ValidatorStatusChangeType
from pycspr.types.node.rpc import WasmModule
from pycspr.types.node.rpc import Weight
from pycspr.utils import constants
from pycspr.utils import convertor


def decode(encoded: dict, typedef: object) -> object:
    """Decoder: Domain entity <- JSON blob.

    :param encoded: A JSON compatible dictionary.
    :param typedef: Deploy related type definition.
    :returns: A deploy related type.

    """
    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json")
    else:
        return decoder(encoded)


def _decode_account_info(encoded: dict) -> AccountInfo:
    return AccountInfo(
        address=decode(encoded["account_hash"], Address),
        action_thresholds=decode(encoded["action_thresholds"], ActionThresholds),
        associated_keys=[decode(i, AssociatedKey) for i in encoded["associated_keys"]],
        main_purse=decode(encoded["main_purse"], URef),
        named_keys=[decode(i, NamedKey) for i in encoded["named_keys"]],
    )


def _decode_action_thresholds(encoded: dict) -> ActionThresholds:
    return ActionThresholds(
        deployment=decode(encoded["deployment"], Weight),
        key_management=decode(encoded["key_management"], Weight),
    )


def _decode_address(encoded: str) -> Address:
    if encoded.startswith("account-hash-"):
        return decode(encoded[13:], bytes)
    else:
        return decode(encoded, bytes)


def _decode_associated_key(encoded: dict) -> AssociatedKey:
    return AssociatedKey(
        address=decode(encoded["account_hash"], Address),
        weight=decode(encoded["weight"], Weight),
        )


def _decode_auction_bid_by_delegator(encoded: dict) -> AuctionBidByDelegator:
    return AuctionBidByDelegator(
        bonding_purse=decode(encoded["bonding_purse"], URef),
        delegatee=decode(encoded["delegatee"], PublicKeyBytes),
        public_key=decode(encoded["public_key"], PublicKeyBytes),
        staked_amount=decode(encoded["staked_amount"], Motes),
    )


def _decode_auction_bid_by_validator(encoded: dict) -> AuctionBidByValidator:
    return AuctionBidByValidator(
        public_key=decode(encoded["public_key"], PublicKeyBytes),
        bid=decode(encoded["bid"], AuctionBidByValidatorInfo),
    )


def _decode_auction_bid_by_validator_info(encoded: dict) -> AuctionBidByValidatorInfo:
    return AuctionBidByValidatorInfo(
        bonding_purse=decode(encoded["bonding_purse"], URef),
        # TODO: verify
        delegation_rate=decode(encoded["delegation_rate"], int),
        delegators=[decode(i, AuctionBidByDelegator) for i in encoded["delegators"]],
        inactive=decode(encoded["inactive"], bool),
        staked_amount=decode(encoded["staked_amount"], Motes),
    )


def _decode_auction_state(encoded: dict) -> AuctionState:
    return AuctionState(
        bids=[decode(i, AuctionBidByValidator) for i in encoded["bids"]],
        block_height=decode(encoded["block_height"], BlockHeight),
        era_validators=[decode(i, EraValidators) for i in encoded["era_validators"]],
        state_root=decode(encoded["state_root_hash"], Digest),
    )


def _decode_block(encoded: dict) -> Block:
    return Block(
        body=decode(encoded["body"], BlockBody),
        hash=decode(encoded["hash"], Digest),
        header=decode(encoded["header"], BlockHeader),
        proofs=[decode(i, BlockSignature) for i in encoded["proofs"]],
    )


def _decode_block_body(encoded: dict) -> BlockBody:
    return BlockBody(
        proposer=decode(encoded["proposer"], PublicKeyBytes),
        deploy_hashes=[decode(i, Digest) for i in encoded["deploy_hashes"]],
        transfer_hashes=[decode(i, Digest) for i in encoded["transfer_hashes"]],
    )


def _decode_block_header(encoded: dict) -> BlockHeader:
    return BlockHeader(
        accumulated_seed=decode(encoded["accumulated_seed"], bytes),
        body_hash=decode(encoded["body_hash"], Digest),
        era_id=decode(encoded["era_id"], EraID),
        height=decode(encoded["height"], BlockHeight),
        parent_hash=decode(encoded["parent_hash"], Digest),
        protocol_version=decode(encoded["protocol_version"], ProtocolVersion),
        random_bit=decode(encoded["random_bit"], bool),
        state_root=decode(encoded["state_root_hash"], Digest),
        )


def _decode_block_signature(encoded: dict) -> BlockSignature:
    return BlockSignature(
        public_key=decode(encoded["public_key"], PublicKeyBytes),
        signature=decode(encoded["signature"], SignatureBytes)
    )


def _decode_block_transfers(encoded: dict) -> BlockTransfers:
    return BlockTransfers(
        block_hash=decode(encoded["block_hash"], Digest),
        transfers=[decode(i, Transfer) for i in encoded["transfers"]],
    )


def _decode_deploy(encoded: dict) -> Deploy:
    return Deploy(
        approvals=[decode(i, DeployApproval) for i in encoded["approvals"]],
        hash=decode(encoded["hash"], Digest),
        header=decode(encoded["header"], DeployHeader),
        payment=decode(encoded["payment"], DeployExecutableItem),
        session=decode(encoded["session"], DeployExecutableItem)
    )


def _decode_deploy_approval(encoded: dict) -> DeployApproval:
    return DeployApproval(
        signer=create_public_key_from_account_key(
            decode(encoded["signer"], AccountKey)
            ),
        signature=decode(encoded["signature"], SignatureBytes),
    )


def _decode_deploy_argument(encoded: typing.Tuple[str, dict]) -> DeployArgument:
    return DeployArgument(
        name=decode(encoded[0], str),
        value=decode_cl_value(encoded[1])
        )


def _decode_deploy_execution_info(encoded: list) -> DeployExecutionInfo:
    print("TODO: _decode_deploy_execution_info")
    return encoded


def _decode_deploy_executable_item(encoded: dict) -> DeployExecutableItem:
    def _decode_deploy_of_module_bytes(encoded) -> DeployOfModuleBytes:
        if "ModuleBytes" in encoded:
            encoded = encoded["ModuleBytes"]

        return DeployOfModuleBytes(
            args=[decode(i, DeployArgument) for i in encoded["args"]],
            module_bytes=decode(encoded["module_bytes"], bytes),
            )

    def _decode_deploy_of_stored_contract_by_hash(encoded) -> DeployOfStoredContractByHash:
        if "StoredContractByHash" in encoded:
            encoded = encoded["StoredContractByHash"]

        return DeployOfStoredContractByHash(
            args=[decode(i, DeployArgument) for i in encoded["args"]],
            entry_point=decode(encoded["entry_point"], str),
            hash=decode(encoded["hash"], Digest),
        )

    def _decode_deploy_of_stored_contract_by_hash_versioned(encoded) -> DeployOfStoredContractByHashVersioned:
        if "StoredVersionedContractByHash" in encoded:
            encoded = encoded["StoredVersionedContractByHash"]

        return DeployOfStoredContractByHashVersioned(
            args=[decode(i, DeployArgument) for i in encoded["args"]],
            entry_point=decode(encoded["entry_point"], str),
            hash=decode(encoded["hash"], Digest),
            version=decode(encoded["version"], int),
        )

    def _decode_deploy_of_stored_contract_by_name(encoded) -> DeployOfStoredContractByName:
        if "StoredContractByName" in encoded:
            encoded = encoded["StoredContractByName"]

        return DeployOfStoredContractByName(
            args=[decode(i, DeployArgument) for i in encoded["args"]],
            entry_point=decode(encoded["entry_point"], str),
            name=decode(encoded["name"], str),
        )

    def _decode_deploy_of_stored_contract_by_name_versioned(encoded) -> DeployOfStoredContractByNameVersioned:
        if "StoredVersionedContractByName" in encoded:
            encoded = encoded["StoredVersionedContractByName"]

        return DeployOfStoredContractByNameVersioned(
            args=[decode(i, DeployArgument) for i in encoded["args"]],
            entry_point=decode(encoded["entry_point"], str),
            name=decode(encoded["name"], str),
            version=decode(encoded["version"], int),
        )

    def _decode_deploy_of_transfer(encoded) -> DeployOfTransfer:
        if "Transfer" in encoded:
            encoded = encoded["Transfer"]

        return DeployOfTransfer(
            args=[decode(i, DeployArgument) for i in encoded["args"]],
            )

    if "ModuleBytes" in encoded:
        decoder = _decode_deploy_of_module_bytes
    elif "StoredContractByHash" in encoded:
        decoder = _decode_deploy_of_stored_contract_by_hash
    elif "StoredVersionedContractByHash" in encoded:
        decoder = _decode_deploy_of_stored_contract_by_hash_versioned
    elif "StoredContractByName" in encoded:
        decoder = _decode_deploy_of_stored_contract_by_name
    elif "StoredVersionedContractByName" in encoded:
        decoder = _decode_deploy_of_stored_contract_by_name_versioned
    elif "Transfer" in encoded:
        decoder = _decode_deploy_of_transfer
    else:
        raise NotImplementedError(f"Unsupported DeployExecutableItem variant: {encoded}")
    
    return decoder(encoded)


def _decode_deploy_header(encoded: dict) -> DeployHeader:
    decode(encoded["ttl"], DeployTimeToLive)

    return DeployHeader(
        account=create_public_key_from_account_key(
            decode(encoded["account"], bytes)
        ),
        body_hash=decode(encoded["body_hash"], bytes),
        chain_name=decode(encoded["chain_name"], str),
        dependencies=[decode(i, Digest) for i in encoded["dependencies"]],
        gas_price=decode(encoded["gas_price"], GasPrice),
        timestamp=decode(encoded["timestamp"], Timestamp),
        ttl=decode(encoded["ttl"], DeployTimeToLive)
    )


def _decode_deploy_time_to_live(encoded: str) -> DeployTimeToLive:
    as_ms = convertor.ms_from_humanized_time_interval(encoded)
    if as_ms > constants.DEPLOY_TTL_MS_MAX:
        raise ValueError(f"Invalid deploy ttl. Maximum (ms)={constants.DEPLOY_TTL_MS_MAX}")

    return DeployTimeToLive(as_ms, encoded)


def _decode_era_info(encoded: dict) -> EraInfo:
    return EraInfo(
        seigniorage_allocations=[
            decode(i, SeigniorageAllocation) for i in encoded["seigniorage_allocations"]
            ]
    )


def _decode_era_validators(encoded: dict) -> EraValidators:
    return EraValidators(
        era_id=decode(encoded["era_id"], EraID),
        validator_weights=[decode(i, EraValidatorWeight) for i in encoded["validator_weights"]]
    )


def _decode_era_validator_weight(encoded: dict) -> EraValidatorWeight:
    return EraValidatorWeight(
        public_key=decode(encoded["public_key"], PublicKeyBytes),
        weight=decode(encoded["weight"], Weight)
    )


def _decode_era_summary(encoded: dict) -> EraSummary:
    return EraSummary(
        block_hash=decode(encoded["block_hash"], Digest),
        era_id=decode(encoded["era_id"], EraID),
        era_info=decode(encoded["stored_value"]["EraInfo"], EraInfo),
        merkle_proof=decode(encoded["merkle_proof"], MerkleProofBytes),
        state_root=decode(encoded["state_root_hash"], Digest),
    )


def _decode_named_key(encoded: dict) -> NamedKey:
    return NamedKey(
        key=decode(encoded["key"], str),
        name=decode(encoded["name"], str),
    )


def _decode_node_status(encoded: dict) -> NodeStatus:
    return NodeStatus(
        api_version=decode(encoded["api_version"], str),
    )


def _decode_protocol_version(encoded: str) -> ProtocolVersion:
    major, minor, revision = encoded.split(".")

    return ProtocolVersion(
        major=int(major),
        minor=int(minor),
        revision=int(revision)
        )


def _decode_seigniorage_allocation(encoded: dict) -> SeigniorageAllocation:
    def decode_delegator_seigniorage_allocation(encoded: dict):
        return SeigniorageAllocationForDelegator(
            amount=decode(encoded["amount"], Motes),
            delegator_public_key=decode(encoded["delegator_public_key"], PublicKeyBytes),
            validator_public_key=decode(encoded["validator_public_key"], PublicKeyBytes),
        )

    def decode_validator_seigniorage_allocation(encoded: dict):
        return SeigniorageAllocationForValidator(
            amount=decode(encoded["amount"], Motes),
            validator_public_key=decode(encoded["validator_public_key"], PublicKeyBytes),
        )

    if "Delegator" in encoded:
        return decode_delegator_seigniorage_allocation(encoded["Delegator"])
    elif "Validator" in encoded:
        return decode_validator_seigniorage_allocation(encoded["Validator"])
    else:
        raise ValueError("decode_seigniorage_allocation")


def _decode_stored_value(encoded: dict) -> typing.Union[EraInfo]:
    if "EraInfo" in encoded:
        _decode_era_info(encoded["EraInfo"])


def _decode_timestamp(encoded: str) -> Timestamp:
    return Timestamp(convertor.timestamp_from_iso_datetime(encoded))


def _decode_transfer(encoded: dict) -> Transfer:
    return Transfer(
        amount=decode(encoded["amount"], Motes),
        deploy_hash=decode(encoded["deploy_hash"], Digest),
        from_=decode(encoded["from"], Address),
        gas=decode(encoded["gas"], Gas),
        source=decode(encoded["source"], URef),
        target=decode(encoded["target"], URef),
        correlation_id=decode(encoded["id"], int),
        to_=decode(encoded["to"], Address),
    )


def _decode_uref(encoded: str) -> URef:
    # E.G. uref-bc4f1cd8cbb7a47464ea82e5dbd045c99f6c2fabedd54df1f50b08fbb9ed35ca-007.
    return URef(
        access_rights=decode(encoded[-3:], URefAccessRights),
        address=decode(encoded[5:-4], Address),
    )


def _decode_uref_access_rights(encoded: str) -> URefAccessRights:
    return URefAccessRights(int(encoded))


def _decode_validator_status_change(encoded: dict) -> ValidatorStatusChange:
    return ValidatorStatusChange(
        era_id=decode(encoded["era_id"], EraID),
        status_change=ValidatorStatusChangeType[encoded["validator_change"]]
    )


def _decode_validator_changes(encoded: list) -> ValidatorChanges:
    return ValidatorChanges(
        public_key=decode(encoded["public_key"], PublicKeyBytes),
        status_changes=[decode(i, ValidatorStatusChange) for i in encoded["status_changes"]],
    )


_DECODERS = {
    bool: bool,
    bytes: lambda x: bytes.fromhex(x),
    int: int,
    str: lambda x: x.strip(),
} | {
    AccountKey: lambda x: decode(x, bytes),
    Address: _decode_address,
    BlockHeight: lambda x: decode(x, int),
    ContractVersion: lambda x: decode(x, int),
    Digest: lambda x: decode(x, bytes),
    EraID: lambda x: decode(x, int),
    Gas: lambda x: decode(x, int),
    GasPrice: lambda x: decode(x, int),
    PublicKeyBytes: lambda x: decode(x, bytes),
    MerkleProofBytes: lambda x: decode(x, bytes),
    Motes: lambda x: decode(x, int),
    SignatureBytes: lambda x: decode(x, bytes),
    Weight: lambda x: decode(x, int),
    WasmModule: lambda x: decode(x, bytes),
} | {
    AccountInfo: _decode_account_info,
    ActionThresholds: _decode_action_thresholds,
    AssociatedKey: _decode_associated_key,
    AuctionBidByDelegator: _decode_auction_bid_by_delegator,
    AuctionBidByValidator: _decode_auction_bid_by_validator,
    AuctionBidByValidatorInfo: _decode_auction_bid_by_validator_info,
    AuctionState: _decode_auction_state,
    Block: _decode_block,
    BlockBody: _decode_block_body,
    BlockHeader: _decode_block_header,
    BlockSignature: _decode_block_signature,
    BlockTransfers: _decode_block_transfers,
    Deploy: _decode_deploy,
    DeployApproval: _decode_deploy_approval,
    DeployArgument: _decode_deploy_argument,
    DeployExecutionInfo: _decode_deploy_execution_info,
    DeployExecutableItem: _decode_deploy_executable_item,
    DeployHeader: _decode_deploy_header,
    DeployOfModuleBytes: _decode_deploy_executable_item,
    DeployOfStoredContractByHash: _decode_deploy_executable_item,
    DeployOfStoredContractByHashVersioned: _decode_deploy_executable_item,
    DeployOfStoredContractByName: _decode_deploy_executable_item,
    DeployOfStoredContractByNameVersioned: _decode_deploy_executable_item,
    DeployOfTransfer: _decode_deploy_executable_item,
    DeployTimeToLive: _decode_deploy_time_to_live,
    EraInfo: _decode_era_info,
    EraValidators: _decode_era_validators,
    EraValidatorWeight: _decode_era_validator_weight,
    EraSummary: _decode_era_summary,
    NamedKey: _decode_named_key,
    NodeStatus: _decode_node_status,
    ProtocolVersion: _decode_protocol_version,
    SeigniorageAllocation: _decode_seigniorage_allocation,
    Timestamp: _decode_timestamp,
    Transfer: _decode_transfer,
    URef: _decode_uref,
    URefAccessRights: _decode_uref_access_rights,
    ValidatorChanges: _decode_validator_changes,
    ValidatorStatusChange: _decode_validator_status_change,
}
