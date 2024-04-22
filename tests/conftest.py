import os
import pytest
from typing import Optional
from evm_wallet import NetworkInfo
from evm_wallet import AsyncWallet, Wallet
from evm_wallet.types import Network, ERC20Token
from web3 import AsyncWeb3


@pytest.fixture(scope="session")
def make_wallet():
    def _make_wallet(
            network: Network | NetworkInfo,
            private_key: Optional[str] = None,
            is_async: bool = True
    ) -> AsyncWallet | Wallet:
        if not private_key:
            private_key = os.getenv('TEST_PRIVATE_KEY')
        return AsyncWallet(private_key, network) if is_async else Wallet(private_key, network)

    return _make_wallet


@pytest.fixture(scope="session")
def eth_amount():
    amount = AsyncWeb3.to_wei(0.001, 'ether')
    return amount


@pytest.fixture(scope="session")
def usdc(make_wallet) -> ERC20Token:
    wallet = make_wallet('BSC', is_async=False)
    return wallet.get_token('0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d')
