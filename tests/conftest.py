import pytest
from evm_wallet import *
from web3 import AsyncWeb3
from evm_wallet.types import NetworkInfo, Network
from dotenv import dotenv_values

dotenv_values = dotenv_values()


@pytest.fixture(scope="session")
def make_wallet():
    def _make_wallet(network: Network | NetworkInfo, is_async: bool = False):
        private_key = dotenv_values.get('TEST_PRIVATE_KEY')
        return AsyncWallet(private_key, network) if is_async else Wallet(private_key, network)

    return _make_wallet


@pytest.fixture(scope="session")
def eth_amount():
    amount = AsyncWeb3.to_wei(0.001, 'ether')
    return amount
