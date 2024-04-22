import pytest


@pytest.fixture()
def wallet(make_wallet):
    return make_wallet(network='BSC', is_async=True)


@pytest.mark.asyncio
async def test_get_balance(wallet):
    balance = await wallet.get_balance()
    assert isinstance(balance, int)


@pytest.mark.asyncio
async def test_build_tx_params(wallet):
    tx_params = await wallet.build_tx_params(0)
    assert 'value' in tx_params and 'gasPrice' in tx_params


@pytest.mark.asyncio
async def test_get_balance_of(wallet, usdc):
    assert isinstance(await wallet.get_balance_of(usdc), int)
