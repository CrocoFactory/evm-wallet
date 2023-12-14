from web3.contract import AsyncContract
from web3.types import Wei
from eth_typing import Address, ChecksumAddress
from typing import Union, Literal, TypedDict
from typing import NotRequired

TokenAmount = Union[Wei, int]
AddressLike = Union[Address, ChecksumAddress, str]
Network = Literal['Arbitrum Goerli', 'Arbitrum', 'Avalanche', 'Base', 'Base Goerli', 'BSC', 'BSC Testnet', 'Ethereum',
                  'Fantom', 'Fantom Testnet', 'Fuji', 'Goerli', 'Linea', 'Linea Goerli', 'Mumbai', 'opBNB',
                  'opBNB Testnet', 'Optimism', 'Optimism Goerli', 'Polygon', 'Sepolia', 'zkSync']

NativeToken = Literal['AGOR', 'ARB', 'BNB', 'tBNB', 'ETH', 'GETH', 'SETH', 'MATIC', 'OP',
                      '0x0000000000000000000000000000000000000000']

ABI = list[str]
ContractMap = dict[str, AsyncContract | ABI]


class NetworkInfo(TypedDict):
    network: str
    rpc: str
    token: str
    chain_id: NotRequired[int]
    explorer: NotRequired[str]


NetworkOrInfo = Union[Network, NetworkInfo]
