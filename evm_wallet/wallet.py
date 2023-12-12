import asyncio
from web3 import AsyncWeb3, Web3
from web3.types import Wei, TxParams, TxData
from hexbytes import HexBytes
from .exceptions import InvalidNetworkInfo
from .globals import NETWORK_MAP
from .types import AddressLike, TokenAmount, Network, NetworkInfo, NetworkOrInfo, NativeToken
from eth_account import Account
from typing import Optional, Self
from eth_typing import ChecksumAddress
from web3.contract.contract import ContractFunction
from .utils import in_literal, load_token_contract, is_typed_dict, is_native_token


class AsyncWallet:
    """
    Async version of Wallet, interacting with your ethereum digital wallet.
    You can change a network of the wallet at any time using network setter
    """
    def __init__(
            self,
            private_key: str,
            network: NetworkOrInfo = 'Ethereum',
    ):
        """
        :param private_key: A private key of existing account
        :param network: Name of supported network to be interacted or custom information about network represented as
        type NetworkInfo
        """
        network_info = self.__validate_network(network)
        rpc = network_info['rpc']
        self.__network = network_info
        self.__provider = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))

        temp_provider = Web3(Web3.HTTPProvider(rpc))

        self.__private_key = private_key
        self.__account = Account.from_key(private_key)
        self.__public_key = self.__provider.to_checksum_address(self.__account.address)
        self.__nonce = temp_provider.eth.get_transaction_count(self.__public_key)
        self.__chain_id = temp_provider.eth.chain_id

    @property
    def provider(self) -> AsyncWeb3:
        return self.__provider

    @property
    def network(self) -> NetworkInfo:
        """
        You can change a network of the wallet at any time using network setter
        :return: Dictionary containing information about the network
        """
        return self.__network

    @network.setter
    def network(self, value: NetworkOrInfo):
        network_info = self.__validate_network(value)
        rpc = network_info['rpc']
        self.__network = network_info
        self.__provider = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))

        temp_provider = Web3(Web3.HTTPProvider(rpc))
        self.__nonce = temp_provider.eth.get_transaction_count(self.__public_key)
        self.__chain_id = temp_provider.eth.chain_id

    @property
    def private_key(self) -> str:
        """
        The private key of the current account
        :return: The private key of the current account
        """
        return self.__private_key

    @property
    def public_key(self) -> ChecksumAddress:
        """
        The public key of the current account
        :return: The public key of the current account
        """
        return self.__public_key

    @property
    def nonce(self) -> int:
        """
        The nonce of the current wallet.
        :return: The nonce of the current wallet
        """
        return self.__nonce

    @property
    def native_token(self) -> str:
        return self.network['token']

    def is_native_token(self, token: NativeToken) -> bool:
        """
        Returns true if token is native token of network

        :param token: Name of token or zero-address - 0x0000000000000000000000000000000000000000
        :return: True if token is native token of network
        """
        return is_native_token(self.network, token)

    @classmethod
    def create(cls, network: NetworkOrInfo = 'Ethereum') -> Self:
        """
        Creates all-new digital wallet
        :param network: Name of supported network to be interacted or custom information about network represented as
        type NetworkInfo
        :return: An instance of AsyncWallet
        """
        network = cls.__validate_network(network)

        private_key = Account.create().key
        return cls(private_key, network)

    @staticmethod
    def __validate_network(network: NetworkOrInfo = 'Ethereum') -> NetworkInfo:
        if in_literal(network, Network):
            network_info = NetworkInfo(network=network, **NETWORK_MAP[network])
            return network_info
        elif is_typed_dict(network, NetworkInfo):
            return network
        else:
            raise InvalidNetworkInfo(network)

    async def get_balance(self) -> int:
        """
        Returns the balance of the current account in ethereum units.
        :return: Balance of the current account in ethereum units
        """
        provider = self.provider
        balance = await provider.eth.get_balance(self.public_key)
        return provider.from_wei(balance, 'ether')

    async def estimate_gas(self, tx_data: TxData) -> Wei:
        """
        Returns an estimating quantity of gas to perform transaction in Wei units
        :param tx_data: Data of built transaction
        :return: Estimated gas in Wei
        """
        provider = self.provider
        gas = Wei(int(await provider.eth.estimate_gas(tx_data)))
        return gas

    async def build_and_transact(
            self,
            closure: ContractFunction,
            value: TokenAmount = 0,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None
    ) -> HexBytes:
        """
        If you don't need to check estimated gas or directly use transact, you can call build_and_transact. It's based on getting
        closure as argument. Closure is transaction's function, called with arguments. Notice that it has to be not built or
        awaited

        Usage Example
        ----------
            wallet = AsyncWallet(private_key)

            uniswap = provider.eth.contract(address=address, abi=abi)

            closure = uniswap.functions.swapExactETHForTokens(arg1, arg2, ...)

            await wallet.build_and_transact(closure, eth_amount)

        :param closure: Transaction's function, called with arguments. Notice that it has to be not built or awaited
        :param value: A quantity of network currency to be paid in Wei units
        :param gas: A quantity of gas to be spent
        :param gas_price: A price of gas in Wei units
        :return: Transaction's hash
        """
        provider = self.provider
        tx_params = await self.build_transaction_params(value, gas, gas_price)
        tx_data = await closure.build_transaction(tx_params)

        if not gas:
            del tx_data['gas']
            gas = Wei(int(await provider.eth.estimate_gas(tx_data)))
            tx_data['gas'] = gas

        return await self.transact(tx_data)

    async def approve(
            self,
            token: AddressLike,
            contract_address: AddressLike,
            token_amount: TokenAmount
    ) -> HexBytes:
        """
        Approves token usage for the specific contract
        :param token: An address of token
        :param contract_address: An address of contract that will be using token
        :param token_amount: A quantity of token to be spent in Wei units
        :return: Transaction hash
        """
        token = load_token_contract(self.provider, token)
        return await self.build_and_transact(
            token.functions.approve(contract_address, token_amount)
        )

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
        :return: Transaction's params
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

    async def transact(self, tx_data: TxData) -> HexBytes:
        """
        Performs transaction, using transaction data, which is got after building
        :param tx_data: Built transaction's data
        :return: Transaction's hash
        """
        provider = self.provider
        signed_transaction = provider.eth.account.sign_transaction(tx_data, self.private_key)
        tx_hash = await provider.eth.send_raw_transaction(signed_transaction.rawTransaction)
        self.__nonce += 1
        
        return tx_hash

    async def transfer(
            self,
            token: AddressLike,
            recipient: AddressLike,
            token_amount: TokenAmount,
            gas: Optional[Wei] = None,
            gas_price: Optional[Wei] = None
    ) -> HexBytes:
        """
        Transfers token amount to another wallet
        :param token: An address of token
        :param recipient: An address of the recipient
        :param token_amount: A quantity of token to be transferred in Wei units
        :param gas: A quantity of gas to be spent
        :param gas_price: A price of gas in Wei units
        :return: Transaction hash
        """
        token_contract = load_token_contract(self.provider, token)
        recipient = self.provider.to_checksum_address(recipient)
        closure = await token_contract.functions.transfer(recipient, token_amount)
        return await self.build_and_transact(closure, Wei(0), gas, gas_price)

    async def get_transactions(self) -> list[TxData]:
        """
        Returns a list of transactions for the current wallet
        :return: List of transactions
        """
        provider = self.provider

        block_number = provider.eth.block_number
        start_block = 0
        end_block = block_number

        public_key = self.public_key

        transactions = []
        for block in range(end_block, start_block - 1, -1):
            block_info = await provider.eth.get_block(block, True)

            for tx in reversed(block_info['transactions']):
                if public_key.lower() in [tx['from'].lower(), tx['to'].lower()]:
                    transactions.append(tx)

        return transactions

    def get_explorer_url(self, transaction_hash: HexBytes) -> str:
        """
        Returns the explorer url for the given transaction hash
        :return: Explorer url for the given transaction
        """
        explorer_url = f'Transaction: {self.network["explorer"]}/tx/{transaction_hash}'
        return explorer_url


class Wallet(AsyncWallet):
    """
    Interacts with your ethereum digital wallet.
    You can change a network of the wallet at any time using network setter
    """
    def __init__(
            self,
            private_key: str,
            network: NetworkOrInfo = 'Ethereum',
    ):
        """
        :param private_key: A private key of existing account
        :param network: Name of supported network to be interacted or custom information about network represented as
        type NetworkInfo
        """
        super().__init__(private_key, network)

    def get_balance(self) -> int:
        """
        Returns the balance of the current account in ethereum units.
        :return: Balance of the current account in ethereum units
        """
        async_method = super().get_balance
        return asyncio.run(async_method())

    def estimate_gas(self, tx_data: TxData) -> Wei:
        """
        Returns an estimating quantity of gas to perform transaction in Wei units
        :param tx_data: Data of built transaction
        :return: Estimated gas in Wei
        """
        async_method = super().estimate_gas
        return asyncio.run(async_method(tx_data))

    def build_and_transact(
            self,
            closure: ContractFunction,
            value: Wei = 0,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None
    ) -> HexBytes:
        """
        If you don't need to check estimated gas or directly use transact, you can call build_and_transact. It's based on getting
        closure as argument. Closure is transaction's function, called with arguments. Notice that it has to be not built or
        awaited

        Usage Example
        -------
            wallet = AsyncWallet(private_key)

            uniswap = provider.eth.contract(address=address, abi=abi)

            closure = uniswap.functions.swapExactETHForTokens(arg1, arg2, ...)

            await wallet.build_and_transact(closure, eth_amount)

        :param closure: Transaction's function, called with arguments. Notice that it has to be not built or awaited
        :param value: A quantity of network currency to be paid in Wei units
        :param gas: A quantity of gas to be spent
        :param gas_price: A price of gas in Wei units
        :return: Transaction's hash
        """
        async_method = super().build_and_transact
        return asyncio.run(async_method(closure, value, gas, gas_price))

    def approve(
            self,
            token: AddressLike,
            contract_address: AddressLike,
            token_amount: TokenAmount
    ) -> HexBytes:
        """
        Approves token usage for the specific contract
        :param token: An address of token
        :param contract_address: An address of contract that will be using token
        :param token_amount: A quantity of token to be spent in Wei units
        :return: Transaction hash
        """
        async_method = super().approve
        return asyncio.run(async_method(token, contract_address, token_amount))

    def build_transaction_params(
            self,
            value: Wei,
            gas: Optional[int] = None,
            gas_price: Optional[Wei] = None
    ) -> TxParams:
        """
        Returns transaction's params
        :param value: A quantity of network currency to be paid in Wei units
        :param gas: A quantity of gas to be spent
        :param gas_price: A price of gas in Wei units
        :return: Transaction's params
        """
        async_method = super().build_transaction_params
        return asyncio.run(async_method(value, gas, gas_price))

    def transact(self, tx_data: TxData) -> HexBytes:
        """
        Performs transaction, using transaction data, which is got after building
        :param tx_data: Built transaction's data
        :return: Transaction's hash
        """
        async_method = super().transact
        return asyncio.run(async_method(tx_data))

    async def transfer(
            self,
            token: AddressLike,
            recipient: AddressLike,
            token_amount: TokenAmount,
            gas: Optional[Wei] = None,
            gas_price: Optional[Wei] = None
    ) -> HexBytes:
        """
        Transfers token amount to another wallet
        :param token: An address of token
        :param recipient: An address of the recipient
        :param token_amount: A quantity of token to be transferred in Wei units
        :param gas: A quantity of gas to be spent
        :param gas_price: A price of gas in Wei units
        :return: Transaction hash
        """
        async_method = super().transfer
        return asyncio.run(async_method(token, recipient, token_amount, gas, gas_price))

    def get_transactions(self) -> list[TxData]:
        """
        Returns a list of transactions for the current wallet
        :return: List of transactions
        """
        async_method = super().get_transactions
        return asyncio.run(async_method())
