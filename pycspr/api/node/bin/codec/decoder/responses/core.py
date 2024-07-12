import typing

from pycspr.api.node.bin.codec.decoder.primitives import \
    decode_u8, \
    decode_u16, \
    decode_u32
from pycspr.api.node.bin.types import \
    Response, \
    ResponseHeader
from pycspr.api.node.bin.types.domain import \
    ProtocolVersion


def decode_protocol_version(bstream: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bstream, major = decode_u32(bstream)
    bstream, minor = decode_u32(bstream)
    bstream, patch = decode_u32(bstream)

    return bstream, ProtocolVersion(major, minor, patch)


def decode_response(bstream: bytes) -> typing.Tuple[bytes, Response]:
    bstream, header = decode_response_header(bstream)

    return b'', Response(header, payload=bstream)


def decode_response_header(bstream: bytes) -> typing.Tuple[bytes, ResponseHeader]:
    bstream, protocol_version = decode_protocol_version(bstream)
    bstream, error = decode_u16(bstream)
    bstream, returned_data_type_tag = decode_u8(bstream)

    return bstream, ResponseHeader(
        protocol_version=protocol_version,
        error=error,
        returned_data_type_tag=returned_data_type_tag
    )


DECODERS: typing.Dict[typing.Type, typing.Callable] = {
    Response: decode_response,
    ResponseHeader: decode_response_header,
    ProtocolVersion: decode_protocol_version,
}
