from typing import Literal, get_args, TypedDict, Type, Any, cast
from eth_utils import is_text, is_hex_address, to_checksum_address
from evm_wallet.types import NetworkInfo


def _in_literal(value: Any, expected_type: Literal) -> bool:
    values = get_args(expected_type)
    return value in values


def _has_keys(value: Any, typed_dict: Type[TypedDict]) -> bool:
    typed_dict_keys = typed_dict.__annotations__.keys()

    try:
        value_keys = value.keys()
    except AttributeError:
        return False

    return typed_dict_keys == value_keys


def _is_network_info(value: Any) -> bool:
    if _has_keys(value, NetworkInfo):
        return True
    else:
        try:
            value_keys = value.keys()
        except AttributeError:
            return False

        if set(value_keys) == {'network', 'rpc', 'token'}:
            return True

    return False


def is_checksum_address(value: Any) -> bool:
    if not is_text(value):
        return False

    if not is_hex_address(value):
        return False

    is_equal = value.lower() == to_checksum_address(value).lower()
    return cast(bool, is_equal)
