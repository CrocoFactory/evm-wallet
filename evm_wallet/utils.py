import json
import os
from functools import lru_cache
from typing import Literal, get_args, TypedDict, Type, Any
from web3 import AsyncWeb3
from web3.contract import AsyncContract
from evm_wallet.globals import ZERO_ADDRESS
from evm_wallet.types import ABI, AddressLike, NetworkInfo, NativeToken


def in_literal(value: Any, expected_type: Literal) -> bool:
    values = get_args(expected_type)
    return value in values


def is_typed_dict(value: Any, typed_dict: Type[TypedDict]) -> bool:
    typed_dict_keys = typed_dict.__annotations__.keys()

    try:
        value_keys = value.keys()
    except AttributeError:
        return False

    return typed_dict_keys == value_keys


@lru_cache()
def get_erc20_abi() -> ABI:
    abs_path = os.path.dirname(os.path.abspath(__file__))
    path = f"{abs_path}/erc20.abi"
    with open(path) as file:
        return json.load(file)


def load_token_contract(provider: AsyncWeb3, address: AddressLike) -> AsyncContract:
    address = provider.to_checksum_address(address)
    abi = get_erc20_abi()
    contract = provider.eth.contract(address=address, abi=abi)
    return contract


def is_native_token(network: NetworkInfo, name_or_address: NativeToken) -> bool:
    native_token = network['token']
    return (name_or_address.upper() == native_token or name_or_address.lower() == name_or_address
            or name_or_address == ZERO_ADDRESS)
