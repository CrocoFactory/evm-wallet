from web3.types import Wei
from dataclasses import dataclass
from eth_typing import Address, HexAddress,  ChecksumAddress
from typing import Union, Literal, TypedDict, NotRequired

TokenAmount = Union[Wei, int]
AnyAddress = Union[Address, HexAddress, ChecksumAddress, bytes, str]
Network = Literal['Arbitrum Goerli', 'Arbitrum Sepolia', 'Arbitrum', 'Avalanche', 'Base', 'Base Sepolia', 'Base Goerli',
                  'BSC', 'BSC Testnet', 'Ethereum', 'Fantom', 'Fantom Testnet', 'Fuji', 'Goerli', 'Linea', 'Linea Goerli',
                  'Mumbai', 'opBNB', 'opBNB Testnet', 'Optimism', 'Optimism Goerli', 'Optimism Sepolia', 'Polygon',
                  'Sepolia', 'Scroll', 'zkSync']


@dataclass(frozen=True, kw_only=True)
class ERC20Token:
    address: ChecksumAddress
    symbol: str
    decimals: int


class NetworkInfo(TypedDict):
    network: str
    rpc: str
    token: str
    chain_id: NotRequired[int]
    explorer: NotRequired[str]
