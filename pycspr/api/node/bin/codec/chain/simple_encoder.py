from pycspr.api.node.bin.codec.chain.constants import \
    TAG_BLOCK_HASH, \
    TAG_BLOCK_HEIGHT
from pycspr.api.node.bin.codec.utils import encode, register_encoders
from pycspr.api.node.bin.types.chain import \
    BlockHash, \
    BlockHeight, \
    BlockID, \
    EraID, \
    ProtocolVersion
from pycspr.api.node.bin.types.primitives.numeric import U8, U64


def _encode_block_hash(entity: BlockHash) -> bytes:
    return encode(TAG_BLOCK_HASH, U8) + entity


def _encode_block_height(entity: BlockHeight) -> bytes:
    return encode(TAG_BLOCK_HEIGHT, U8) + encode(entity, U64)


def _encode_block_id(entity: BlockID) -> bytes:
    if isinstance(entity, bytes):
        return encode_block_hash(entity)
    elif isinstance(entity, int):
        return encode_block_height(entity)
    elif isinstance(entity, str):
        print(123, entity.decode("utf-8"))
        return encode_block_hash(entity.decode("utf-8"))
    else:
        raise ValueError("Invalid block identifier")


def _encode_era_id(entity: EraID) -> bytes:
    return encode(TAG_BLOCK_HEIGHT, U8) + encode(entity, U64)


def _encode_protocol_version(entity: ProtocolVersion) -> bytes:
    return encode(entity.major, U8) + encode(entity.minor, U8) + encode(entity.patch, U8)


register_encoders({
    (BlockHash, _encode_block_hash),
    (BlockHeight, _encode_block_height),
    (BlockID, _encode_block_id),
    (EraID, _encode_era_id),
    (ProtocolVersion, _encode_protocol_version),
})
