import pytest


@pytest.fixture()
def wallet(make_wallet):
    return make_wallet(network='Goerli', is_async=True)


@pytest.mark.asyncio
async def test_get_balance(wallet):
    balance = await wallet.get_balance()
    assert balance
