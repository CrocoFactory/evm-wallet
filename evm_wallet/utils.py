import json
import os
from functools import lru_cache
from typing import Literal, get_args, TypedDict, Type, Any
from web3 import AsyncWeb3
from web3.contract import AsyncContract
from web3.types import ABI
from evm_wallet.types import AnyAddress


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


@lru_cache()
def get_erc20_abi() -> ABI:
    abs_path = os.path.dirname(os.path.abspath(__file__))
    path = f"{abs_path}/erc20.abi"
    with open(path) as file:
        return json.load(file)


@lru_cache()
def load_token_contract(provider: AsyncWeb3, address: AnyAddress) -> AsyncContract:
    address = provider.to_checksum_address(address)
    abi = get_erc20_abi()
    contract = provider.eth.contract(address=address, abi=abi)
    return contract
