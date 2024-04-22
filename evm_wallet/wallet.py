from typing import Optional
from eth_typing import HexStr
from eth_utils import is_checksum_address
from hexbytes import HexBytes
from web3 import Web3
from web3.contract.contract import ContractFunction, Contract
from web3.types import TxParams, Wei
from evm_wallet._base_wallet import _BaseWallet
from evm_wallet.types import Network, NetworkInfo, TokenAmount, AnyAddress, ERC20Token


class Wallet(_BaseWallet):
    """
    The class, interacting with your ethereum digital wallet.
    You can change a network of the wallet at any time using network setter
    """

    def __init__(
            self,
            private_key: str,
            network: Network | NetworkInfo = 'Ethereum',
    ):
        """
        :param private_key: Private key of existing account
        :param network: Name of supported network to be interacted or custom information about network represented as
        type NetworkInfo
        """
        super().__init__(private_key, network, False)

    @property
    def provider(self) -> Web3:
        return self._provider

    def _load_token_contract(self, address: AnyAddress) -> Contract:
        return super()._load_token_contract(address)

    def get_balance(self, from_wei: bool = False) -> float | Wei:
        """
        Returns the balance of the current account in ethereum or wei units.
        :param from_wei: Whether to convert balance to Ether units (default: False)
        :return: Balance of the current account in ethereum units
        """
        provider = self.provider
        balance = provider.eth.get_balance(self.public_key)

        return balance if not from_wei else provider.from_wei(balance, 'ether')

    def estimate_gas(self, tx_params: TxParams, from_wei: bool = False) -> Wei:
        """
        Returns an estimating quantity of gas to perform transaction in Wei units
        :param tx_params: Params of built transaction
        :param from_wei: Whether to convert balance to Ether units (default: False)
        :return: Estimated gas in Wei
        """
        provider = self.provider
        gas = Wei(int(provider.eth.estimate_gas(tx_params)))
        return gas if not from_wei else provider.from_wei(gas, 'ether')

    def build_and_transact(
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
            wallet = Wallet(private_key)

            uniswap = provider.eth.contract(address=address, abi=abi)

            closure = uniswap.functions.swapExactETHForTokens(arg1, arg2, ...)

            wallet.build_and_transact(closure, eth_amount)

        :param closure: Transaction's function, called with arguments. Notice that it has to be not built or awaited
        :param value: Quantity of network currency to be paid in Wei units
        :param gas: Quantity of gas to be spent
        :param gas_price: Price of gas in Wei units
        :return: Transaction's hash
        """
        tx_params = self.build_tx_params(value=value, gas=gas, gas_price=gas_price)
        tx_params = closure.build_transaction(tx_params)

        return self.transact(tx_params)

    def approve(
            self,
            token: ERC20Token,
            contract_address: AnyAddress,
            token_amount: TokenAmount
    ) -> HexBytes:
        """
        Approves token usage for the specific contract
        :param token: ERC20Token instance
        :param contract_address: Address of contract that will be using token
        :param token_amount: Quantity of token to be spent in Wei units
        :return: Transaction hash
        """
        if not is_checksum_address(contract_address):
            raise ValueError('Invalid contract address is provided')

        token = self._load_token_contract(token.address)
        contract_address = self.provider.to_checksum_address(contract_address)
        return self.build_and_transact(
            token.functions.approve(contract_address, token_amount)
        )

    def build_tx_params(
            self,
            value: TokenAmount,
            recipient: Optional[AnyAddress] = None,
            raw_data: Optional[bytes | HexStr] = None,
            gas: Optional[Wei] = Wei(300_000),
            gas_price: Optional[Wei] = None
    ) -> TxParams:
        """
        Returns transaction's params
        :param value: Quantity of network currency to be paid in Wei units
        :param recipient: Address of recipient
        :param raw_data: Transaction's data provided as HexStr or bytes
        :param gas: Quantity of gas to be spent
        :param gas_price: Price of gas in Wei units
        :return: Transaction's params
        """
        provider = self.provider

        tx_params = {
            'from': self.public_key,
            'chainId': self.network['chain_id'],
            'nonce': self.nonce,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price if gas_price else provider.eth.gas_price,
        }

        if recipient:
            tx_params['to'] = provider.to_checksum_address(recipient)

        if raw_data:
            tx_params['data'] = raw_data

        return tx_params

    def transact(self, tx_params: TxParams) -> HexBytes:
        """
        Performs transaction, using transaction params, which are got after building
        :param tx_params: Built transaction's params
        :return: Transaction hash
        """
        provider = self.provider
        signed_transaction = provider.eth.account.sign_transaction(tx_params, self.private_key)
        tx_hash = provider.eth.send_raw_transaction(signed_transaction.rawTransaction)
        self._nonce += 1

        return tx_hash

    def transfer(
            self,
            token: ERC20Token,
            recipient: AnyAddress,
            token_amount: TokenAmount,
            gas: Optional[Wei] = None,
            gas_price: Optional[Wei] = None
    ) -> HexBytes:
        """
        Transfers token amount to another wallet
        :param token: ERC20Token instance
        :param recipient: Address of the recipient
        :param token_amount: Quantity of token to be transferred in Wei units
        :param gas: Quantity of gas to be spent
        :param gas_price: Price of gas in Wei units
        :return: Transaction hash
        """
        if not is_checksum_address(recipient):
            raise ValueError('Invalid recipient address is provided')

        token_contract = self._load_token_contract(token.address)
        recipient = self.provider.to_checksum_address(recipient)
        closure = token_contract.functions.transfer(recipient, token_amount)
        return self.build_and_transact(closure, Wei(0), gas, gas_price)

    def get_balance_of(self, token: ERC20Token, convert: bool = False) -> float:
        """
        Returns balance of specified token in ethereum or wei units
        :param token: ERC20Token instance
        :param convert: Whether to divide token balance by its decimals (default: False)
        :return: Balance of specified token in ethereum or wei units
        """
        token_contract = self._load_token_contract(token.address)
        balance = token_contract.functions.balanceOf(self.public_key).call()

        if convert:
            balance /= 10 ** token.decimals

        return balance

    def get_token(self, address: AnyAddress) -> ERC20Token:
        """
        Returns ERC20 token, containing information about it
        :param address: address of the token
        :return: ERC20Token instance
        """
        if not is_checksum_address(address):
            raise ValueError('Invalid token address is provided')

        address = self._provider.to_checksum_address(address)
        token_contract = self._load_token_contract(address)
        symbol = token_contract.functions.symbol().call()
        decimals = token_contract.functions.decimals().call()

        return ERC20Token(address=address, symbol=symbol, decimals=decimals)
