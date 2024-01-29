from web3.contract import AsyncContract
from web3.types import Wei, ABI
from eth_typing import Address, HexAddress,  ChecksumAddress
from typing import Union, Literal, TypedDict
from typing import NotRequired

TokenAmount = Union[Wei, int]
AnyAddress = Union[Address, HexAddress, ChecksumAddress, str]
Network = Literal['Arbitrum Goerli', 'Arbitrum', 'Avalanche', 'Base', 'Base Goerli', 'BSC', 'BSC Testnet', 'Ethereum',
                  'Fantom', 'Fantom Testnet', 'Fuji', 'Goerli', 'Linea', 'Linea Goerli', 'Mumbai', 'opBNB',
                  'opBNB Testnet', 'Optimism', 'Optimism Goerli', 'Polygon', 'Sepolia', 'zkSync']

ContractMap = dict[str, AsyncContract | ABI]


class NetworkInfo(TypedDict):
    network: str
    rpc: str
    token: str
    chain_id: NotRequired[int]
    explorer: NotRequired[str]


NetworkOrInfo = Union[Network, NetworkInfo]
