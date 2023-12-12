"""
evm-wallet
~~~~~~~~~~~~~~
The package, containing wrapper over EVM operations for interacting through Wallet units.
Author github - https://github.com/blnkoff

Usage example:
   >>> from evm_wallet import Wallet
   >>> arb_wallet = Wallet('your_private_key', 'Arbitrum')
   >>> provider = arb_wallet.provider
   >>> recipient = '0xe977Fa8D8AE7D3D6e28c17A868EF04bD301c583f'
   >>> usdt = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
   >>> usdt_amount = provider.to_wei(0.001)
   >>>
   >>> if arb_wallet.get_balance() >= 0.01:
   >>>     arb_wallet.transfer(usdt, recipient, usdt_amount)

:copyright: (c) 2023 by Alexey
:license: Apache 2.0, see LICENSE for more details.
"""

__version__ = "1.0.0"

from .wallet import AsyncWallet, Wallet
from .types import NetworkInfo
from .globals import ZERO_ADDRESS
