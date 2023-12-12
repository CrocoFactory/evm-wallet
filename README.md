# evm-wallet

[![Croco Logo](https://i.ibb.co/G5Pjt6M/logo.png)](https://t.me/crocofactory)


The package, containing wrapper over EVM operations for interacting through Wallet entities.

- **[Telegram channel](https://t.me/crocofactory)**
- **[Overview](#quick-overview)**
- **[Bug reports](https://github.com/blnkoff/evm-wallet/issues)**


Web3.py suggests to interact with instance of Web3 as primary entity. We offer way to use Wallet entity, that is more 
familiar, since we try to provide the similar to digital wallet apps' logic. We introduce:
 
- possibility to set and change current wallet's network by network's name
- swift and robust performing transactions
- quick performing useful functions of Web3.py
   
evm-wallet's source code is made available under the [MIT License](LICENSE)

##  Quick start
You can quickly use supported networks as RPC:  

| Network         | Native Token | Testnet  |
|-----------------|--------------|----------|
| Arbitrum Goerli | AGOR         | ✅        |
| Arbitrum        | ETH          | ❌        |
| Avalanche       | AVAX         | ❌        |
| Base            | ETH          | ❌        |
| Base Goerli     | ETH          | ✅        |
| BSC             | BNB          | ❌        |
| BSC Testnet     | tBNB         | ✅        |
| Ethereum        | ETH          | ❌        |
| Fantom          | FTM          | ❌        |
| Fantom Testnet  | FTM          | ✅        |
| Fuji            | AVAX         | ✅        |
| Goerli          | GETH         | ✅        |
| Linea           | ETH          | ❌        |
| Linea Goerli    | ETH          | ✅        |
| Mumbai          | MATIC        | ✅        |
| opBNB           | BNB          | ❌        |
| opBNB Testnet   | BNB          | ✅        |
| Optimism        | ETH          | ❌        |
| Optimism Goerli | OGOR         | ✅        |
| Polygon         | MATIC        | ❌        |
| Sepolia         | SETH         | ❌        |
| zkSync          | ETH          | ❌        |



For specifying network you only need to pass network's name.
```python
from evm_wallet import Wallet
arb_wallet = Wallet('your_private_key', 'Arbitrum')
```

If you use unsupported network, you can specify it using type NetworkInfo
```python
from evm_wallet import Wallet, NetworkInfo

network_info = NetworkInfo(
    network='Custom',
    rpc='https://custom.publicnode.com',
    token='CUSTOM'
)
custom_wallet = Wallet('your_private_key', network_info)
```

evm-wallet also asynchronous approach
```python
from evm_wallet import AsyncWallet

async def validate_balance():
    async_wallet = AsyncWallet('your_private_key', 'Arbitrum')
    balance = await async_wallet.get_balance()
    assert balance > 0.1
```
     
<h2 id="#quick-overview">Quick overview</h2> 
You can perform the following actions, using evm-wallet:

- **[approve](#approve)**
- **[build_and_transact](#build_and_transact)**
- **[build_transaction_params](#build_transaction_params)**
- **[create](#create)**
- **[estimate_gas](#estimate_gas)**
- **[get_balance](#get_balance)**
- **[get_explorer_url](#get_explorer_url)**
- **[get_transactions](#get_transactions)**
- **[is_native_token](#is_native_token)**
- **[transact](#transact)**
- **[transfer](#transfer)**

<h3 id="approve">approve</h3>

When you want to spend non-native tokens, for instance USDT, you need to perform approving operation.

```python
from evm_wallet import Wallet
arb_wallet = Wallet('your_private_key', 'Arbitrum')
provider = arb_wallet.provider

stargate_router = '0x8731d54E9D02c286767d56ac03e8037C07e01e98'
usdt = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
usdt_amount = provider.to_wei(0.001, 'ether')

arb_wallet.approve(usdt, stargate_router, usdt_amount)
```

<h3 id="build_and_transact">build_and_transact</h3>
If you don't need to check estimated gas or directly use transact, you can call build_and_transact. It's based on getting
closure as argument. Closure is transaction's function, called with arguments. Notice that it has to be not built or 
awaited

```python
from evm_wallet import Wallet
from web3.contract import Contract
arb_wallet = Wallet('your_private_key', 'Arbitrum')
provider = arb_wallet.provider

stargate_router = '0x8731d54E9D02c286767d56ac03e8037C07e01e98'
stargate_abi = [...]
stargate = Contract(stargate_router, stargate_abi)

eth_amount = provider.to_wei(0.001, 'ether')
closure = stargate.functions.swapETH(...) 
arb_wallet.build_and_transact(closure, eth_amount)
```

<h3 id="build_transaction_params">build_transaction_params</h3>
You can use build_transaction_params to quickly get dictionary of params for building transaction. Public key, chain id 
and nonce are generated automatically. You also can also choose not to set a gas and the gas price

```python
async def build_transaction_params(
        self,
        value: TokenAmount,
        gas: Optional[int] = None,
        gas_price: Optional[Wei] = None
) -> TxParams:
    """
    Returns transaction's params
    :param value: A quantity of network currency to be paid in Wei units
    :param gas: A quantity of gas to be spent
    :param gas_price: A price of gas in Wei units
    :return: TxParams
    """
    provider = self.provider

    tx_params = {
        'from': self.public_key,
        'chainId': self.__chain_id,
        'nonce': self.nonce,
        'value': value,
        'gas': gas if gas else Wei(250_000),
        'gasPrice': gas_price if gas_price else await provider.eth.gas_price,
    }
    return tx_params
```

<h3 id="create">create</h3>
You can use that, when you want to create all-new wallet

```python
from evm_wallet import Wallet
wallet = Wallet.create('Arbitrum')
```
            
<h3 id="estimate_gas">estimate_gas</h3>
When you want to estimate an amount of gas to send a transaction, you can use estimate_gas

```python
from evm_wallet import Wallet
from web3.contract import Contract
arb_wallet = Wallet('your_private_key', 'Arbitrum')
provider = arb_wallet.provider

stargate_router = '0x8731d54E9D02c286767d56ac03e8037C07e01e98'
stargate_abi = [...]
eth_amount = provider.to_wei(0.001, 'ether')

stargate = Contract(stargate_router, stargate_abi)
params = arb_wallet.build_transaction_params(eth_amount)
tx_data = stargate.functions.swapETH(...).buildTransaction(params)
gas = arb_wallet.estimate_gas(tx_data)
tx_data['gas'] = gas
```

<h3 id="get_balance">get_balance</h3>
You can get the balance of your wallet at any moment.

```python
from evm_wallet import Wallet
arb_wallet = Wallet('your_private_key', 'Arbitrum')
balance = arb_wallet.get_balance()
```
            
<h3 id="get_explorer_url">get_explorer_url</h3>
You can get entire wallet's list of transactions

```python
from evm_wallet import Wallet
from web3.contract import Contract
arb_wallet = Wallet('your_private_key', 'Arbitrum')
provider = arb_wallet.provider

stargate_router = '0x8731d54E9D02c286767d56ac03e8037C07e01e98'
stargate_abi = [...]
stargate = Contract(stargate_router, stargate_abi)

eth_amount = provider.to_wei(0.001, 'ether')
closure = stargate.functions.swapETH(...) 
tx_hash = arb_wallet.build_and_transact(closure, eth_amount)
print(arb_wallet.get_explorer_url(tx_hash))
```


<h3 id="get_transactions">get_transactions</h3>
You can get entire wallet's list of transactions

```python
from evm_wallet import Wallet
arb_wallet = Wallet('your_private_key', 'Arbitrum')
transactions = arb_wallet.get_transactions()
```

<h3 id="is_native_token">is_native_token</h3>
If you want to check, if the specific token is native token of network, you can use is_native_token.

You can use any case in a token's ticker.
```python
from evm_wallet import Wallet
arb_wallet = Wallet('your_private_key', 'Arbitrum')
assert arb_wallet.is_native_token('eTh')
```

Or you can pass zero-address meaning address of network's native token.
```python
from evm_wallet import Wallet, ZERO_ADDRESS
arb_wallet = Wallet('your_private_key', 'Arbitrum')
assert arb_wallet.is_native_token(ZERO_ADDRESS)
```

<h3 id="transact">transact</h3>
After building transaction you can perform it, passing transaction data to transact

```python
from evm_wallet import Wallet
from web3.contract import Contract
arb_wallet = Wallet('your_private_key', 'Arbitrum')
provider = arb_wallet.provider

stargate_router = '0x8731d54E9D02c286767d56ac03e8037C07e01e98'
stargate_abi = [...]
eth_amount = provider.to_wei(0.001, 'ether')

stargate = Contract(stargate_router, stargate_abi)
params = arb_wallet.build_transaction_params(eth_amount)
tx_data = stargate.functions.swapETH(...).buildTransaction(params)
gas = arb_wallet.estimate_gas(tx_data)
tx_data['gas'] = gas

arb_wallet.transact(tx_data)
```

<h3 id="transfer">transfer</h3>
You can transfer tokens to another wallet

```python
from evm_wallet import Wallet
arb_wallet = Wallet('your_private_key', 'Arbitrum')
provider = arb_wallet.provider

recipient = '0xe977Fa8D8AE7D3D6e28c17A868EF04bD301c583f'
usdt = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
usdt_amount = provider.to_wei(0.001, 'ether')

arb_wallet.transfer(usdt, recipient, usdt_amount)
```



# Installing evm-wallet
        
To install the package from GitHub you can use:

```shell
pip install git+https://github.com/blnkoff/evm-wallet.git
```

To install the package from PyPi you can use:
```shell
pip install evm-wallet
```

