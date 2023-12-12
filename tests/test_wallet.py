import pytest


@pytest.fixture
def wallet(make_wallet):
    return make_wallet(network='Goerli')


def test_get_balance(wallet):
    balance = wallet.get_balance()
    assert balance
