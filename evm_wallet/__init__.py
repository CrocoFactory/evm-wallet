"""
evm-wallet
~~~~~~~~~~~~~~
The package, containing wrapper over EVM operations for interacting through Wallet units.
Author github - https://github.com/blnkoff

Usage example:
   >>> from evm_wallet import Wallet
   >>> my_wallet = Wallet('your_private_key', 'Arbitrum')
   >>> provider = my_wallet.provider
   >>> recipient = '0xe977Fa8D8AE7D3D6e28c17A868EF04bD301c583f'
   >>> 
   >>> usdt = my_wallet.get_token('0xdAC17F958D2ee523a2206206994597C13D831ec7')
   >>> usdt_amount = provider.to_wei(0.001)
   >>>
   >>> if my_wallet.get_balance() >= 0.01:
   >>>     my_wallet.transfer(usdt, recipient, usdt_amount)

:copyright: (c) 2023 by Alexey
:license: MIT, see LICENSE for more details.
"""
import warnings
from .wallet import Wallet
from .async_wallet import AsyncWallet
from .types import NetworkInfo, ERC20Token
from ._base_wallet import ZERO_ADDRESS

warnings.warn(
    "This package has been deprecated. You should migrate to `https://github.com/CrocoFactory/ether`, "
    "because this package will be deleted in few months",
    DeprecationWarning,
    stacklevel=2
)

warnings.simplefilter('always', DeprecationWarning)
